from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re

from builtins import *
from past.builtins import *
from future import standard_library
standard_library.install_aliases()
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
from mapr.ojai.exceptions.AccessDeniedError import AccessDeniedError
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
from mapr.ojai.utils.retry_utils import retry_if_connection_not_established, RetryOptions, \
    DEFAULT_WAIT_EXPONENTIAL_MULTIPLIER, DEFAULT_WAIT_EXPONENTIAL_MAX, DEFAULT_STOP_MAX_ATTEMPT
import urllib.parse
import logging

LOG = logging.getLogger(__name__)


class OJAIConnection(Connection):

    def __init__(self, connection_str, options=None):

        if options is None:
            options = {}

        if not isinstance(options, dict):
            raise TypeError('Options type must be dict.')
        self.__retry_config = \
            RetryOptions(options.get('ojai.mapr.rpc.wait-multiplier',
                                     DEFAULT_WAIT_EXPONENTIAL_MULTIPLIER),
                         options.get('ojai.mapr.rpc.wait-max-attempt',
                                     DEFAULT_WAIT_EXPONENTIAL_MAX),
                         options.get('ojai.mapr.rpc.max-retries',
                                     DEFAULT_STOP_MAX_ATTEMPT))
        self.__url, self.__auth, self.__encoded_user_metadata, self.__ssl, \
        self.__ssl_ca, self.__ssl_target_name_override = OJAIConnection.__parse_connection_url(
            connection_str=connection_str)

        self.__channel = OJAIConnection.__get_channel(self.__url,
                                                      self.__ssl,
                                                      self.__ssl_ca,
                                                      self.__ssl_target_name_override,
                                                      self.__encoded_user_metadata)

        self.__connection = MapRDbServerStub(self.__channel)
        self.__configure_retry(self.__retry_config)
        self.__ping_connection(self.__connection)
        LOG.debug('Connection was created'
                  ' for %s with options auth:%s, ssl:%s, sslTargetNameOverride:%s',
                  self.__url,
                  self.__auth,
                  self.__ssl,
                  self.__ssl_target_name_override)

    def __configure_retry(self, retry_config):
        retry_dec = retry(
            wait_exponential_multiplier=retry_config.wait_exponential_multiplier,
            wait_exponential_max=retry_config.wait_exponential_max,
            stop_max_attempt_number=retry_config.stop_max_attempt_number,
            retry_on_exception=retry_if_connection_not_established
        )
        self.__ping_connection = retry_dec(self.__ping_connection)
        self.create_store = retry_dec(self.create_store)
        self.is_store_exists = retry_dec(self.is_store_exists)
        self.delete_store = retry_dec(self.delete_store)

    def __ping_connection(self, connection):
        try:
            connection.Ping(PingRequest(), timeout=10)
        except _Rendezvous as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                raise ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise e

    @staticmethod
    def __parse_connection_url(connection_str):
        try:
            url, options = re.sub('ojai:mapr:thin:v1@', '',
                                  connection_str).split('?', 1)
        except TypeError as e:
            raise IllegalArgumentError(
                m='Connection string type must be str, but was {0}. \n{1}'
                    .format(type(connection_str), e))
        except ValueError as e:
            raise ValueError('{0}. \n{1}'
                             .format(e,
                                     'Common url string format'
                                     ' is <host>[:<port>][?<options...>].'))

        options_dict = dict()
        for pair in urllib.parse.urlparse(connection_str).query.split(';'):
            entry = pair.split('=')
            if entry[1:]:
                options_dict[entry[0]] = urllib.parse.unquote(entry[1])

        key = '{0}:{1}'.format(options_dict.get('user', ''), options_dict.get('password', '')).encode()
        encoded_user_metadata = base64.b64encode(key).decode()
        ssl = json.loads(options_dict.get('ssl', 'true'))
        ssl_ca = options_dict.get('sslCA', '')

        if ssl and not ssl_ca:
            raise AttributeError(
                'sslCa path must be specified when ssl enabled.')

        return url, \
               options_dict.get('auth', 'basic'), \
               encoded_user_metadata, \
               ssl, \
               ssl_ca, \
               options_dict.get('sslTargetNameOverride', '')

    @staticmethod
    def __get_channel(url,
                      ssl,
                      ssl_ca,
                      ssl_target_name_override,
                      encoded_user_metadata):
        interceptor = auth_interceptor.client_auth_interceptor(encoded_user_metadata)
        if ssl:
            # Disabling SSL validation is currently not supported by gRPC Python library
            # https://github.com/grpc/grpc/pull/15274
            with open(ssl_ca, 'rb') as f:
                ssl_trust_pem = f.read()
            ssl_credentials = \
                grpc.ssl_channel_credentials(ssl_trust_pem)
            if ssl_target_name_override:
                channel = grpc.secure_channel(url,
                                              ssl_credentials,
                                              (('grpc.ssl_target_name_override',
                                                ssl_target_name_override),))
            else:
                channel = grpc.secure_channel(url,
                                              ssl_credentials)
        else:
            channel = grpc.insecure_channel(url)
        return grpc.intercept_channel(channel, interceptor)

    def create_store(self, store_path):
        self.__validate_store_path(store_path=store_path)
        request = CreateTableRequest(table_path=store_path)
        LOG.debug('Sending CREATE STORE request to the server. Request body: %s', request)
        response = self.__connection.CreateTable(request)
        LOG.debug('Got CREATE STORE response from the server. Response body: %s', response)

        if self.__validate_response(response=response):
            return self.get_store(store_path=store_path)

    def is_store_exists(self, store_path):
        self.__validate_store_path(store_path=store_path)
        request = TableExistsRequest(table_path=store_path)
        LOG.debug('Sending IS STORE EXISTS request to the server. Request body: %s', request)
        response = self.__connection.TableExists(request)
        LOG.debug('Got IS STORE EXISTS response from the server. Response body: %s', response)
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
            raise UnknownServerError(m=response.error.error_message)

    def delete_store(self, store_path):
        self.__validate_store_path(store_path=store_path)
        request = DeleteTableRequest(table_path=store_path)
        LOG.debug('Sending DELETE STORE request to the server. Request body: %s', request)
        response = self.__connection.DeleteTable(request)
        LOG.debug('Got DELETE STORE response from the server. Response body: %s', response)
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
        elif response.error.err_code == ErrorCode.Value('ACCESS_DENIED'):
            raise AccessDeniedError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('TABLE_NOT_FOUND'):
            return False
        else:
            raise UnknownServerError(m=response.error.error_message)

    @staticmethod
    def __validate_store_path(store_path):
        if not isinstance(store_path, basestring):
            raise TypeError

    def get_or_create_store(self, store_path):
        if self.is_store_exists(store_path=store_path):
            return self.get_store(store_path=store_path)
        else:
            return self.create_store(store_path=store_path)

    def get_store(self, store_path):
        LOG.debug('Trying to get store %s from the server.', store_path)
        if self.is_store_exists(store_path=store_path):
            return OJAIDocumentStore(url=self.__url,
                                     store_path=store_path,
                                     connection=self.__connection,
                                     retry_config=self.__retry_config)
        else:
            raise StoreNotFoundError(m='Store {0} not found.'.format(store_path))

    def new_document(self, json_string=None, dictionary=None):
        doc = OJAIDocument()

        if json_string is None and dictionary is None:
            return doc
        elif dictionary is not None and isinstance(dictionary, dict):
            doc.from_dict(dictionary)
        elif json_string is not None \
                and isinstance(json_string, basestring):
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
