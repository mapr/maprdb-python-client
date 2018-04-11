import json

from ojai.document.DocumentStore import DocumentStore

from mapr.ojai.exceptions.ClusterNotFoundError import ClusterNotFoundError
from mapr.ojai.exceptions.DecodingError import DecodingError
from mapr.ojai.exceptions.DocumentAlreadyExistsError import DocumentAlreadyExistsError
from mapr.ojai.exceptions.EncodingError import EncodingError
from mapr.ojai.exceptions.InvalidOJAIDocumentError import InvalidOJAIDocumentError
from mapr.ojai.exceptions.PathNotFoundError import PathNotFoundError
from mapr.ojai.exceptions.StoreNotFoundError import StoreNotFoundError
from mapr.ojai.exceptions.UnknownPayloadEncodingError import UnknownPayloadEncodingError
from mapr.ojai.exceptions.UnknownServerError import UnknownServerError
from mapr.ojai.exceptions.UnrecognizedInsertModeError import UnrecognizedInsertModeError
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai.OJAIQueryResult import OJAIQueryResult
from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
from mapr.ojai.proto.gen.maprdb_server_pb2 import InsertOrReplaceRequest, PayloadEncoding, FindByIdRequest, ErrorCode, \
    InsertMode, FindRequest


class OJAIDocumentStore(DocumentStore):

    def __init__(self, url, store_path, connection):
        self.__url = url
        self.__store_path = store_path
        self.__connection = connection

    def is_read_only(self):
        pass

    def flush(self):
        pass

    def find_by_id(self, _id, field_paths=None, condition=None, results_as_document=False):
        if not isinstance(_id, (str, unicode)):
            raise TypeError
        doc = OJAIDocument().set_id(_id=_id)
        request = FindByIdRequest(table_path=self.__store_path,
                                  payload_encoding=PayloadEncoding.Value('JSON_ENCODING'),
                                  json_document=doc.as_json_str())

        if request.WhichOneof('data') == 'json_document' \
                and request.payload_encoding == PayloadEncoding.Value('JSON_ENCODING'):
            response = self.__connection.FindById(request)
        else:
            raise UnknownPayloadEncodingError(m='Invalid find_by_id params')

        from mapr.ojai.ojai.OJAIDocumentCreator import OJAIDocumentCreator

        if len(response.json_document) == 0 and results_as_document:
            return OJAIDocumentCreator.create_document("{}")
        elif len(response.json_document) == 0:
            return {}
        elif results_as_document:
            return OJAIDocumentCreator.create_document(json_string=response.json_document)
        else:
            return OJAIDocumentCreator.create_document(json_string=response.json_document).as_dictionary()

    def __parse_find_response(self, response):
        self.validate_response(response)
        response_type = response.type
        if response_type == 0:
            raise UnknownServerError('Unknown response type.')
        elif response_type == 1:
            return response.json_response
        # TODO
        elif response_type == 2:
            return response.json_response
        else:
            raise UnknownServerError('Check server logs.')

    def find(self, query=None, results_as_document=False, include_query_plan=False):
        # json_document_list = []
        if query is None:
            query_str = '{}'
        elif isinstance(query, str):
            query_str = query
        elif isinstance(query, OJAIQuery):
            query_str = query.to_json_str()
        elif isinstance(query, dict):
            query_str = json.dumps(query)
        else:
            raise TypeError

        request = FindRequest(table_path=self.__store_path,
                              payload_encoding=PayloadEncoding.Value('JSON_ENCODING'),
                              include_query_plan=include_query_plan,
                              json_query=query_str)

        response_stream = self.__connection.Find(request)

        return OJAIQueryResult(document_stream=response_stream, results_as_document=results_as_document,
                               include_query_plan=include_query_plan)

    def __evaluate_doc_stream(self, doc_stream, operation_type):
        for doc in doc_stream:
            if isinstance(doc, OJAIDocument):
                self.__validate_dict(doc.as_dictionary())
                doc_str = doc.as_json_str()
            else:
                self.__validate_dict(doc)
                doc_str = OJAIDocument().from_dict(doc).as_json_str()
            response = self.__connection.InsertOrReplace(
                InsertOrReplaceRequest(table_path=self.__store_path,
                                       insert_mode=InsertMode.Value(operation_type),
                                       payload_encoding=PayloadEncoding.Value('JSON_ENCODING'),
                                       json_document=doc_str))
            self.validate_response(response=response)

    def __evaluate_doc(self, doc_str, operation_type):
        response = self.__connection.InsertOrReplace(
            InsertOrReplaceRequest(table_path=self.__store_path,
                                   insert_mode=InsertMode.Value(operation_type),
                                   payload_encoding=PayloadEncoding.Value('JSON_ENCODING'),
                                   json_document=doc_str))
        self.validate_response(response=response)

    def insert_or_replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        if doc_stream is None:
            if doc is not None:
                self.__validate_dict(doc.as_dictionary())
                doc_str = doc.as_json_str()
            elif json_dictionary is not None:
                self.__validate_dict(json_dictionary)
                doc_str = json.dumps(json_dictionary)
            else:
                raise AttributeError
            self.__evaluate_doc(doc_str=doc_str, operation_type='INSERT_OR_REPLACE')
        else:
            self.__evaluate_doc_stream(doc_stream, 'INSERT_OR_REPLACE')

    def update(self, _id, mutation):
        pass

    def delete(self, doc=None, _id=None, field_as_key=None, doc_stream=None):
        pass

    def insert(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        if doc_stream is None:
            if doc is not None:
                self.__validate_dict(doc.as_dictionary())
                doc_str = doc.as_json_str()
            elif json_dictionary is not None:
                self.__validate_dict(json_dictionary)
                doc_str = json.dumps(json_dictionary)
            else:
                raise AttributeError
            self.__evaluate_doc(doc_str=doc_str, operation_type='INSERT')
        else:
            self.__evaluate_doc_stream(doc_stream, 'INSERT')

    def replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        if doc_stream is None:
            if doc is not None:
                self.__validate_dict(doc.as_dictionary())
                doc_str = doc.as_json_str()
            elif json_dictionary is not None:
                self.__validate_dict(json_dictionary)
                doc_str = json.dumps(json_dictionary)
            else:
                raise AttributeError
            self.__evaluate_doc(doc_str=doc_str, operation_type='REPLACE')
        else:
            self.__evaluate_doc_stream(doc_stream, 'REPLACE')

    def increment(self, _id, field, inc):
        pass

    def check_and_mutate(self, _id, query_condition, mutation):
        pass

    def check_and_delete(self, _id, condition):
        pass

    def check_and_replace(self, _id, condition, doc):
        pass

    @staticmethod
    def __validate_document(doc_to_insert):
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        if doc_to_insert is None:
            raise InvalidOJAIDocumentError
        if not isinstance(doc_to_insert, OJAIDocument):
            raise TypeError

        if '_id' in doc_to_insert.as_dictionary() and isinstance(doc_to_insert.as_dictionary()['_id'], (str, unicode)):
            return True

        raise InvalidOJAIDocumentError(m="Invalid OJAI Document")

    @staticmethod
    def __validate_dict(dict_to_insert):
        if not isinstance(dict_to_insert, dict):
            raise TypeError

        if '_id' in dict_to_insert and isinstance(dict_to_insert['_id'], (str, unicode)):
            return True

        raise InvalidOJAIDocumentError(m="Invalid dictionary")

    @staticmethod
    def validate_response(response):
        if response.error.err_code == ErrorCode.Value('NO_ERROR'):
            return
        if response.error.err_code == ErrorCode.Value('CLUSTER_NOT_FOUND'):
            raise ClusterNotFoundError(m=response.error.error_message)
        if response.error.err_code == ErrorCode.Value('UNKNOWN_PAYLOAD_ENCODING'):
            raise UnknownPayloadEncodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('PATH_NOT_FOUND'):
            raise PathNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('TABLE_NOT_FOUND'):
            raise StoreNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('DOCUMENT_ALREADY_EXISTS'):
            raise DocumentAlreadyExistsError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('ENCODING_ERROR'):
            raise EncodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('DECODING_ERROR'):
            raise DecodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('UNRECOGNIZED_INSERT_MODE'):
            raise UnrecognizedInsertModeError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('UNKNOWN_EXCEPTION'):
            raise UnknownServerError('Check server logs.')
