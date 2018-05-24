import json

import grpc
from ojai.store.Connection import Connection
from retrying import retry

from mapr.ojai.document.OJAIDocumentMutation import OJAIDocumentMutation
from mapr.ojai.exceptions.ClusterNotFoundError import ClusterNotFoundError
from mapr.ojai.exceptions.IllegalArgumentError import IllegalArgumentError
from mapr.ojai.exceptions.PathNotFoundError import PathNotFoundError
from mapr.ojai.exceptions.StoreAlreadyExistsError import StoreAlreadyExistsError
from mapr.ojai.exceptions.UnknownServerError import UnknownServerError
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai.OJAIDocumentStore import OJAIDocumentStore
from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.proto.gen.maprdb_server_pb2 import CreateTableRequest, ErrorCode, TableExistsRequest, \
    InsertOrReplaceRequest, DeleteTableRequest
from mapr.ojai.proto.gen.maprdb_server_pb2_grpc import MapRDbServerStub
from mapr.ojai.utils.retry_utils import retry_if_connection_not_established


class OJAIConnection(Connection):

    def __init__(self, connection_url):
        self.__channel = grpc.insecure_channel(connection_url)
        self.__connection = MapRDbServerStub(self.__channel)
        self.__connection_url = connection_url

    @property
    def channel(self):
        return self.__channel

    @retry(wait_exponential_multiplier=1000,
           wait_exponential_max=18000,
           stop_max_attempt_number=7,
           retry_on_exception=retry_if_connection_not_established)
    def create_store(self, store_path):
        self.__validate_store_path(store_path=store_path)
        response = self.__connection.CreateTable(CreateTableRequest(table_path=store_path))
        if self.__validate_response(response=response):
            return self.get_store(store_path=store_path)

    @retry(wait_exponential_multiplier=1000,
           wait_exponential_max=18000,
           stop_max_attempt_number=7,
           retry_on_exception=retry_if_connection_not_established)
    def is_store_exists(self, store_path):
        self.__validate_store_path(store_path=store_path)
        response = self.__connection.TableExists(TableExistsRequest(table_path=store_path))

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
        response = self.__connection.DeleteTable(DeleteTableRequest(table_path=store_path))
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
        return OJAIDocumentStore(url=self.__connection_url,
                                 store_path=store_path,
                                 connection=self.__connection)

    def new_document(self, json_string=None, dictionary=None):
        doc = OJAIDocument()

        if json_string is None and dictionary is None:
            return doc
        elif dictionary is not None and isinstance(dictionary, dict):
            doc.from_dict(dictionary)
        elif json_string is not None\
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
