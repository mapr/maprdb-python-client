from ojai.document.DocumentStore import DocumentStore

from mapr.ojai.exceptions.ClusterNotFoundError import ClusterNotFoundError
from mapr.ojai.exceptions.DecodingError import DecodingError
from mapr.ojai.exceptions.EncodingError import EncodingError
from mapr.ojai.exceptions.InvalidOJAIDocumentError import InvalidOJAIDocumentError
from mapr.ojai.exceptions.PathNotFoundError import PathNotFoundError
from mapr.ojai.exceptions.StoreNotFoundError import StoreNotFoundError
from mapr.ojai.exceptions.UnknownServerError import UnknownServerError
from mapr.ojai.exceptions.UnrecognizedInsertModeError import UnrecognizedInsertModeError
from mapr.ojai.proto.gen.maprdb_server_pb2 import InsertOrReplaceRequest, PayloadEncoding, FindByIdRequest, ErrorCode


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
        if not isinstance(_id, (str, unicode)):
            raise TypeError
        response = self.__connection.FindById(
            FindByIdRequest(table_path=self.__store_path,
                            payload_encoding=PayloadEncoding.Value('JSON_ENCODING'),
                            json_payload=_id))

        return response.error.err

    def find(self, query=None, field_paths=None, condition=None, query_string=None):
        pass

    def insert_or_replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        self.__validate_document(doc_to_insert=doc)
        response = self.__connection.InsertOrReplace(
            InsertOrReplaceRequest(table_path=self.__store_path,
                                   # insert_mode=InsertMode.Value('INSERT_OR_REPLACE'),
                                   payload_encoding=PayloadEncoding.Value('JSON_ENCODING'),
                                   json_payload=doc.as_json_str()))

        self.__validate_response(response)

    def update(self, _id, mutation):
        pass

    def delete(self, doc=None, _id=None, field_as_key=None, doc_stream=None):
        pass

    def insert(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        # self.__validate_document(doc_to_insert=doc)
        # response = self.__connection.InsertOrReplace(
        #     InsertOrReplaceRequest(table_path=self.__store_path,
        #                            insert_mode=InsertMode.Value('INSERT'),
        #                            payload_encoding=PayloadEncoding.Value('JSON_ENCODING'),
        #                            json_payload=doc.as_json_str()))
        #
        # self.__validate_response(response)
        raise NotImplementedError

    def replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        # self.__validate_document(doc_to_insert=doc)
        # response = self.__connection.InsertOrReplace(
        #     InsertOrReplaceRequest(table_path=self.__store_path,
        #                            insert_mode=InsertMode.Value('REPLACE'),
        #                            payload_encoding=PayloadEncoding.Value('JSON_ENCODING'),
        #                            json_payload=doc.as_json_str()))
        #
        # self.__validate_response(response)
        raise NotImplementedError

    def increment(self, _id, field, inc):
        pass

    def check_and_mutate(self, _id, query_condition, mutation):
        pass

    def check_and_delete(self, _id, condition):
        pass

    def check_and_replace(self, _id, condition, doc):
        pass

    def __validate_document(self, doc_to_insert):
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        if doc_to_insert is None:
            raise InvalidOJAIDocumentError
        if not isinstance(doc_to_insert, OJAIDocument):
            raise TypeError

        if '_id' in doc_to_insert.as_dictionary() and isinstance(doc_to_insert.as_dictionary()['_id'], str):
            return True

        raise InvalidOJAIDocumentError

    def __validate_response(self, response):
        if response.error.err == ErrorCode.Value('NO_ERROR'):
            return
        if response.error.err == ErrorCode.Value('CLUSTER_NOT_FOUND'):
            raise ClusterNotFoundError
        elif response.error.err == ErrorCode.Value('PATH_NOT_FOUND'):
            raise PathNotFoundError
        elif response.error.err == ErrorCode.Value('TABLE_NOT_FOUND'):
            raise StoreNotFoundError
        elif response.error.err == ErrorCode.Value('ENCODING_ERROR'):
            raise EncodingError
        elif response.error.err == ErrorCode.Value('DECODING_ERROR'):
            raise DecodingError
        elif response.error.err == ErrorCode.Value('UNRECOGNIZED_INSERT_MODE'):
            raise UnrecognizedInsertModeError
        elif response.error.err == ErrorCode.Value('UNKNOWN_EXCEPTION'):
            raise UnknownServerError
