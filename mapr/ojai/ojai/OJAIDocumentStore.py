from ojai.document.DocumentStore import DocumentStore

from mapr.ojai.proto.gen.maprdb_server_pb2 import InsertOrReplaceRequest, PayloadEncoding


class OJAIDocumentStore(DocumentStore):

    def __init__(self, url, store_path, connection):
        self.__url = url
        self.__store_path = store_path
        self.__connection = connection

    def is_read_only(self):
        pass

    def flush(self):
        pass

    def find_by_id(self, _id, field_paths=None, condition=None):
        pass

    def find(self, query=None, field_paths=None, condition=None, query_string=None):
        pass

    def insert_or_replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        response = self.__connection.InsertOrReplace(
            InsertOrReplaceRequest(table_path=self.__store_path,
                                   payload_encoding=0,
                                   json_payload=doc.as_json_str()))
        print(response.error.err)
        print(response.payload_encoding)
        print(response.json_payload)
        return response.error.err

    def update(self, _id, mutation):
        pass

    def delete(self, doc=None, _id=None, field_as_key=None, doc_stream=None):
        pass

    def insert(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        pass

    def replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        pass

    def increment(self, _id, field, inc):
        pass

    def check_and_mutate(self, _id, query_condition, mutation):
        pass

    def check_and_delete(self, _id, condition):
        pass

    def check_and_replace(self, _id, condition, doc):
        pass