import grpc
from ojai.store.Connection import Connection

from mapr.ojai.exceptions.ClusterNotFoundError import ClusterNotFoundError
from mapr.ojai.exceptions.PathNotFoundError import PathNotFoundError
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai.OJAIDocumentStore import OJAIDocumentStore
from mapr.ojai.proto.gen.maprdb_server_pb2 import CreateTableRequest, ErrorCode, TableExistsRequest, \
    InsertOrReplaceRequest, DeleteTableRequest
from mapr.ojai.proto.gen.maprdb_server_pb2_grpc import MapRDbServerStub


class ConnectionImpl(Connection):

    def __init__(self, connection_url):
        self.__channel = grpc.insecure_channel(connection_url)
        self.__connection = MapRDbServerStub(self.__channel)
        self.__connection_url = connection_url

    @property
    def channel(self):
        return self.__channel

    def create_table(self, table_path):
        response = self.__connection.CreateTable(CreateTableRequest(table_path=table_path))
        if response.error.err == 0:
            return True
        elif response.error.err == 2:
            raise ClusterNotFoundError
        else:
            return False

    def is_table_exists(self, table_path):
        response = self.__connection.TableExists(TableExistsRequest(table_path=table_path))
        if response.error.err == 0:
            return True
        elif response.error.err == 2:
            raise ClusterNotFoundError
        elif response.error.err == 3:
            raise PathNotFoundError
        elif response.error.err == 4:
            return False
        else:
            print "SOMETHING WRONG"
            return False

    def delete_table(self, table_path):
        response = self.__connection.DeleteTable(DeleteTableRequest(table_path=table_path))
        if response.error.err == 0:
            return True
        elif response.error.err == 2:
            raise ClusterNotFoundError
        elif response.error.err == 3:
            raise PathNotFoundError
        elif response.error.err == 4:
            return False
        else:
            print "SOMETHING WRONG"
            return False

    def get_store(self, store_name, options=None):
        return OJAIDocumentStore(url=self.__connection_url, store_path=store_name, connection=self.__connection)

    def new_document(self, json_string=None, dictionary=None):
        doc = OJAIDocument()

        if dictionary is not None:
            for k, v in dictionary.iteritems():
                doc.set(k, v)
        elif json_string is not None:
            # TODO
            print("TODO")
            pass
        else:
            raise AttributeError

        return doc

    def new_mutation(self):
        raise NotImplementedError

    def new_condition(self):
        raise NotImplementedError

    def new_query(self, query_json=None):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
