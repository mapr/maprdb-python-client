import base64
import json

import grpc
from grpc._channel import _Rendezvous
from ojai.store.Connection import Connection
from retrying import retry

from mapr.ojai.document.OJAIDocumentMutation import OJAIDocumentMutation
from mapr.ojai.exceptions.ClusterNotFoundError import ClusterNotFoundError
from mapr.ojai.exceptions.ConnectionError import ConnectionError
from mapr.ojai.exceptions.IllegalArgumentError import IllegalArgumentError
from mapr.ojai.exceptions.PathNotFoundError import PathNotFoundError
from mapr.ojai.exceptions.StoreAlreadyExistsError import StoreAlreadyExistsError
from mapr.ojai.exceptions.StoreNotFoundError import StoreNotFoundError
from mapr.ojai.exceptions.UnknownServerError import UnknownServerError
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.storage.OJAIDocumentStore import OJAIDocumentStore
from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.proto.gen.maprdb_server_pb2 import CreateTableRequest, \
    ErrorCode, TableExistsRequest, DeleteTableRequest, PingRequest
from mapr.ojai.proto.gen.maprdb_server_pb2_grpc import MapRDbServerStub
from mapr.ojai.storage import auth_interceptor
from mapr.ojai.utils.retry_utils import retry_if_connection_not_established
import urlparse


class OJAIConnection(Connection):

    def __init__(self, connection_str):
        self.__url, self.__auth, self.__encoded_user_metadata, self.__ssl, self.__ssl_validation, \
        self.__ssl_ca, self.__ssl_target_name_override = OJAIConnection.__parse_connection_url(
            connection_url=connection_str)

        self.__channel = OJAIConnection.__get_channel(self.__url,
                                                      self.__ssl,
                                                      self.__ssl_validation,
                                                      self.__ssl_ca,
                                                      self.__ssl_target_name_override,
                                                      self.__encoded_user_metadata)

        self.__connection = MapRDbServerStub(self.__channel)
        OJAIConnection.__ping_connection(self.__connection)

    @staticmethod
    @retry(wait_exponential_multiplier=1000,
           wait_exponential_max=18000,
           stop_max_attempt_number=7,
           retry_on_exception=retry_if_connection_not_established)
    def __ping_connection(connection):
        try:
            connection.Ping(PingRequest(), timeout=10)
        except _Rendezvous as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                raise ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise e

    @staticmethod
    def __parse_connection_url(connection_url):
        try:
            url, options = connection_url.split('?')
        except ValueError as e:
            raise ValueError('{0}. \n{1}'
                             .format(e.message,
                                     'Common url string format'
                                     ' is <host>[:<port>][?<options...>].'))
        options_dict = (urlparse.parse_qs(urlparse.urlparse(connection_url).query))
        auth = options_dict.get('auth', ['basic'])[0]
        encoded_user_metadata = base64.b64encode('{0}:{1}'.format(options_dict.get('user', [''])[0],
                                                                  options_dict.get('password', [''])[0]))
        ssl = True if options_dict.get('ssl', ['false'])[0] == 'true' else False
        ssl_validation = True if options_dict.get('sslValidate', ['true'])[0] == 'true' else False
        ssl_ca = options_dict.get('sslCA', [''])[0]
        ssl_target_name_override = options_dict.get('sslTargetNameOverride', [''])[0]

        if ssl and ssl_validation and ssl_ca == '':
            raise AttributeError('sslCa path must be specified when ssl and sslValidation enabled.')

        if ssl and ssl_validation and ssl_target_name_override == '':
            raise AttributeError('sslTargetNameOverride must be specified when sslValidation enabled.')

        return url, auth, encoded_user_metadata, ssl, ssl_validation, ssl_ca, ssl_target_name_override

    @staticmethod
    def __get_channel(url,
                      ssl,
                      ssl_validation,
                      ssl_ca,
                      ssl_target_name_override,
                      encoded_user_metadata):
        interceptor = auth_interceptor.client_auth_interceptor(encoded_user_metadata)
        if ssl:
            if ssl_validation:
                ssl_trust_pem = open(ssl_ca).read()
                ssl_credentials = \
                    grpc.ssl_channel_credentials(root_certificates=ssl_trust_pem)
                channel = grpc.secure_channel(url,
                                              ssl_credentials,
                                              (('grpc.ssl_target_name_override',
                                                ssl_target_name_override),))
                return grpc.intercept_channel(channel, interceptor)
            else:
                raise NotImplementedError("This features not implemented in grpc."
                                          "Track it there: https://github.com/grpc/grpc/pull/15274")
        else:
            channel = grpc.insecure_channel(url)
            return grpc.intercept_channel(channel, interceptor)

    @retry(wait_exponential_multiplier=1000,
           wait_exponential_max=18000,
           stop_max_attempt_number=7,
           retry_on_exception=retry_if_connection_not_established)
    def create_store(self, store_path):
        self.__validate_store_path(store_path=store_path)
        request = CreateTableRequest(table_path=store_path)
        response = self.__connection.CreateTable(request)

        if self.__validate_response(response=response):
            return self.get_store(store_path=store_path)

    @retry(wait_exponential_multiplier=1000,
           wait_exponential_max=18000,
           stop_max_attempt_number=7,
           retry_on_exception=retry_if_connection_not_established)
    def is_store_exists(self, store_path):
        self.__validate_store_path(store_path=store_path)
        request = TableExistsRequest(table_path=store_path)
        response = self.__connection.TableExists(request)
        if response.error.err_code == ErrorCode.Value('NO_ERROR'):
            return True
        elif response.error.err_code == ErrorCode.Value('CLUSTER_NOT_FOUND'):
            raise ClusterNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('TABLE_ALREADY_EXISTS'):
            raise StoreAlreadyExistsError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('PATH_NOT_FOUND'):
            raise PathNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('TABLE_NOT_FOUND'):
            return False
        else:
            raise UnknownServerError

    @retry(wait_exponential_multiplier=1000,
           wait_exponential_max=18000,
           stop_max_attempt_number=7,
           retry_on_exception=retry_if_connection_not_established)
    def delete_store(self, store_path):
        self.__validate_store_path(store_path=store_path)
        request = DeleteTableRequest(table_path=store_path)
        response = self.__connection.DeleteTable(request)
        return self.__validate_response(response=response)

    @staticmethod
    def __validate_response(response):
        if response.error.err_code == ErrorCode.Value('NO_ERROR'):
            return True
        elif response.error.err_code == ErrorCode.Value('CLUSTER_NOT_FOUND'):
            raise ClusterNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('TABLE_ALREADY_EXISTS'):
            raise StoreAlreadyExistsError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('PATH_NOT_FOUND'):
            raise PathNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('TABLE_NOT_FOUND'):
            return False
        else:
            raise UnknownServerError

    @staticmethod
    def __validate_store_path(store_path):
        if not isinstance(store_path, (str, unicode)):
            raise TypeError

    def get_or_create_store(self, store_path, options=None):
        if self.is_store_exists(store_path=store_path):
            return self.get_store(store_path=store_path, options=options)
        else:
            return self.create_store(store_path=store_path)

    def get_store(self, store_path, options=None):
        if self.is_store_exists(store_path=store_path):
            return OJAIDocumentStore(url=self.__url,
                                     store_path=store_path,
                                     connection=self.__connection,
                                     )
        else:
            raise StoreNotFoundError(m='Store {0} not found.'.format(store_path))

    def new_document(self, json_string=None, dictionary=None):
        doc = OJAIDocument()

        if json_string is None and dictionary is None:
            return doc
        elif dictionary is not None and isinstance(dictionary, dict):
            doc.from_dict(dictionary)
        elif json_string is not None \
                and isinstance(json_string, (str, unicode)):
            doc.from_dict(json.loads(json_string))
        else:
            raise IllegalArgumentError(
                m='Optional parameters for document can be only string or dictionary.')

        return doc

    def new_mutation(self):
        return OJAIDocumentMutation()

    def new_condition(self):
        return OJAIQueryCondition()

    def new_query(self, query_json=None):
        ojai_query = OJAIQuery()
        if query_json is not None:
            ojai_query.from_json(query_json)
        return ojai_query

    def close(self):
        del self.__channel
        del self.__connection
