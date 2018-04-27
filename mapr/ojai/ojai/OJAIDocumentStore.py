import json

from ojai.document.DocumentStore import DocumentStore

from mapr.ojai.exceptions.ClusterNotFoundError import ClusterNotFoundError
from mapr.ojai.exceptions.DecodingError import DecodingError
from mapr.ojai.exceptions.DocumentAlreadyExistsError import \
    DocumentAlreadyExistsError
from mapr.ojai.exceptions.EncodingError import EncodingError
from mapr.ojai.exceptions.IllegalArgumentError import IllegalArgumentError
from mapr.ojai.exceptions.InvalidOJAIDocumentError import \
    InvalidOJAIDocumentError
from mapr.ojai.exceptions.PathNotFoundError import PathNotFoundError
from mapr.ojai.exceptions.StoreNotFoundError import StoreNotFoundError
from mapr.ojai.exceptions.UnknownPayloadEncodingError import \
    UnknownPayloadEncodingError
from mapr.ojai.exceptions.UnknownServerError import UnknownServerError
from mapr.ojai.exceptions.UnrecognizedInsertModeError import \
    UnrecognizedInsertModeError
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai.OJAIQueryResult import OJAIQueryResult
from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.proto.gen.maprdb_server_pb2 import InsertOrReplaceRequest, \
    PayloadEncoding, FindByIdRequest, ErrorCode, \
    InsertMode, FindRequest, DeleteRequest, UpdateRequest


class OJAIDocumentStore(DocumentStore):

    def __init__(self, url, store_path, connection):
        self.__url = url
        self.__store_path = store_path
        self.__connection = connection

    def is_read_only(self):
        pass

    def flush(self):
        pass

    @staticmethod
    def __get_str_mutation(mutation):
        from mapr.ojai.document.OJAIDocumentMutation import \
            OJAIDocumentMutation
        if not isinstance(mutation, (OJAIDocumentMutation, dict)):
            raise IllegalArgumentError(
                m='Mutation type must be OJAIDocumentMutation or dict.')
        str_mutation = json.dumps(mutation.as_dict()) \
            if isinstance(mutation, OJAIDocumentMutation) \
            else json.dumps(mutation)
        return str_mutation

    @staticmethod
    def __get_str_condition(condition):
        from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
        if not isinstance(condition, (OJAIQueryCondition, dict)):
            raise IllegalArgumentError(
                m='Condition must be instance of OJAIQueryCondition, dict.')

        str_condition = json.dumps({'$condition': condition}) \
            if isinstance(condition, dict) else json.dumps(
            {'$condition': condition.as_dictionary()}) \
            if isinstance(condition, OJAIQueryCondition) else None
        return str_condition

    @staticmethod
    def __get_doc_str(doc):
        if not isinstance(doc, (OJAIDocument, dict)):
            raise IllegalArgumentError(m="Invalid type of the doc parameter.")
        return doc.as_json_str() if isinstance(doc, OJAIDocument) \
            else OJAIDocument().from_dict(
            doc).as_json_str()

    def __build_find_by_id_result(self, response, results_as_document):
        from mapr.ojai.ojai.OJAIDocumentCreator import OJAIDocumentCreator

        if len(response.json_document) == 0 and results_as_document:
            return OJAIDocumentCreator.create_document("{}")
        elif len(response.json_document) == 0:
            return {}
        elif results_as_document:
            return OJAIDocumentCreator.create_document(
                json_string=response.json_document)
        else:
            return OJAIDocumentCreator.create_document(
                json_string=response.json_document).as_dictionary()

    def find_by_id(self, _id, field_paths=None, condition=None,
                   results_as_document=False, timeout=None):
        if not isinstance(_id, (str, unicode)):
            raise TypeError

        doc = OJAIDocument().set_id(_id=_id)
        if condition is not None:
            if not isinstance(condition, (OJAIQueryCondition, dict)):
                raise IllegalArgumentError(
                    m='Condition must be instance of OJAIQueryCondition, dict.')
            doc.set('$where', condition if isinstance(condition, dict) else condition.as_dictionary())
        if field_paths is not None:
            if not isinstance(condition, (OJAIQueryCondition, dict)):
                raise IllegalArgumentError(
                    m='Field paths must be instance of list, str.')
            doc.set('$select', field_paths if isinstance(field_paths,
                                                         list) else field_paths.split(','))

        request = FindByIdRequest(table_path=self.__store_path,
                                  payload_encoding=PayloadEncoding.Value(
                                      'JSON_ENCODING'),
                                  json_document=doc.as_json_str())

        if request.WhichOneof('data') == 'json_document' \
                and request.payload_encoding == \
                PayloadEncoding.Value('JSON_ENCODING'):
            if timeout is None:
                response = self.__connection.FindById(request)
            else:
                response = self.__connection.FindById(request, timeout=timeout)

        else:
            raise IllegalArgumentError(m='Invalid find_by_id params')

        return self.__build_find_by_id_result(response=response,
                                              results_as_document=results_as_document)

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

    def find(self, query=None, results_as_document=False,
             include_query_plan=False, timeout=None):
        if query is None:
            query_str = '{}'
        elif isinstance(query, str):
            query_str = query
        elif isinstance(query, OJAIQuery):
            query_str = query.to_json_str()
        elif isinstance(query, dict):
            query_str = json.dumps(query)
        else:
            raise IllegalArgumentError(
                m="Invalid type of the query parameter.")

        request = FindRequest(table_path=self.__store_path,
                              payload_encoding=PayloadEncoding.Value(
                                  'JSON_ENCODING'),
                              include_query_plan=include_query_plan,
                              json_query=query_str)

        if timeout is None:
            response_stream = self.__connection.Find(request)
        else:
            response_stream = self.__connection.Find(request, timeout=timeout)

        return OJAIQueryResult(document_stream=response_stream,
                               results_as_document=results_as_document,
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
                                       insert_mode=InsertMode.Value(
                                           operation_type),
                                       payload_encoding=PayloadEncoding.Value(
                                           'JSON_ENCODING'),
                                       json_document=doc_str))
            self.validate_response(response=response)

    def __evaluate_doc(self, doc_str, operation_type, condition=None):
        request = InsertOrReplaceRequest(table_path=self.__store_path,
                                         insert_mode=InsertMode.Value(
                                             operation_type),
                                         payload_encoding=PayloadEncoding
                                         .Value('JSON_ENCODING'),
                                         json_document=doc_str)
        if condition is not None:
            request.json_condition = condition
        response = self.__connection.InsertOrReplace(request)
        self.validate_response(response=response)

    def insert_or_replace(self, doc=None, _id=None, field_as_key=None,
                          doc_stream=None, json_dictionary=None):
        if doc_stream is None:
            doc_str = OJAIDocumentStore.__get_doc_str(doc=doc)
            self.__evaluate_doc(doc_str=doc_str,
                                operation_type='INSERT_OR_REPLACE')
        else:
            self.__evaluate_doc_stream(doc_stream, 'INSERT_OR_REPLACE')

    def __evaluate_delete(self, doc_string):
        request = DeleteRequest(table_path=self.__store_path,
                                payload_encoding=PayloadEncoding.Value(
                                    'JSON_ENCODING'),
                                json_document=doc_string)
        response = self.__connection.Delete(request)
        self.validate_response(response)

    def __delete_doc_stream(self, doc_stream):
        if not isinstance(doc_stream, list):
            raise IllegalArgumentError(
                m="Invalid type of the doc_stream parameter.")

        for doc in doc_stream:
            if isinstance(doc, OJAIDocument):
                self.__evaluate_delete(doc.as_json_str())
            elif isinstance(doc, dict):
                self.__evaluate_delete(
                    OJAIDocument().from_dict(document_dict=doc).as_json_str())
            else:
                raise IllegalArgumentError(
                    m="Invalid type of the doc parameter, must be "
                      "OJAIDocument or dict.")

    def __delete_id_field(self, _id):
        if not isinstance(_id, (str, unicode, bytearray)):
            raise IllegalArgumentError(m="Invalid type of the _id parameter.")
        self.__evaluate_delete(OJAIDocument().set_id(_id=_id).as_json_str())

    def __delete_document(self, document):
        if not isinstance(document, (OJAIDocument, dict)):
            raise IllegalArgumentError(m="Invalid type of the doc parameter.")

        if isinstance(document, OJAIDocument):
            self.__evaluate_delete(document.as_json_str())
        else:
            self.__evaluate_delete(
                OJAIDocument().from_dict(document_dict=document).as_json_str())

    def delete(self, doc=None, _id=None, field_as_key=None, doc_stream=None):
        if doc is not None:
            self.__delete_document(document=doc)
        elif _id is not None:
            self.__delete_id_field(_id=_id)
        elif doc_stream is not None:
            self.__delete_doc_stream(doc_stream=doc_stream)
        else:
            raise IllegalArgumentError(m="Invalid set of the parameters.")

    def insert(self, doc=None, _id=None, field_as_key=None, doc_stream=None,
               json_dictionary=None):
        if doc_stream is None:
            doc_str = OJAIDocumentStore.__get_doc_str(doc=doc)
            self.__evaluate_doc(doc_str=doc_str, operation_type='INSERT')
        else:
            self.__evaluate_doc_stream(doc_stream, 'INSERT')

    def replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None,
                json_dictionary=None):
        if doc_stream is None:
            doc_str = OJAIDocumentStore.__get_doc_str(doc=doc)
            self.__evaluate_doc(doc_str=doc_str, operation_type='REPLACE')
        else:
            self.__evaluate_doc_stream(doc_stream, 'REPLACE')

    def increment(self, _id, field, inc):
        str_doc = OJAIDocument().set_id(_id=_id).as_json_str()
        from mapr.ojai.document.OJAIDocumentMutation import \
            OJAIDocumentMutation
        str_mutation = self.__get_str_mutation(OJAIDocumentMutation()
                                               .increment(field_path=field,
                                                          inc=inc))
        self.__execute_update(_id=str_doc, mutation=str_mutation)

    def __execute_update(self, _id, mutation, condition=None):
        request = UpdateRequest(table_path=self.__store_path,
                                payload_encoding=PayloadEncoding.Value(
                                    'JSON_ENCODING'),
                                json_document=_id,
                                json_mutation=mutation)
        if condition:
            request.json_condition = condition
        response = self.__connection.Update(request)
        self.validate_response(response=response)

    def update(self, _id, mutation):
        str_doc = OJAIDocument().set_id(_id=_id).as_json_str()
        str_mutation = OJAIDocumentStore.__get_str_mutation(mutation)

        self.__execute_update(_id=str_doc,
                              mutation=str_mutation)

    def check_and_update(self, _id, query_condition, mutation):
        str_condition = OJAIDocumentStore.__get_str_condition(query_condition)
        str_doc = OJAIDocument().set_id(_id=_id).as_json_str()
        str_mutation = OJAIDocumentStore.__get_str_mutation(mutation)

        self.__execute_update(_id=str_doc,
                              mutation=str_mutation,
                              condition=str_condition)

    def check_and_delete(self, _id, condition):
        str_condition = OJAIDocumentStore.__get_str_condition(
            condition=condition)
        request = DeleteRequest(table_path=self.__store_path,
                                payload_encoding=PayloadEncoding.Value(
                                    'JSON_ENCODING'),
                                json_condition=str_condition,
                                json_document=OJAIDocument().set_id(
                                    _id=_id).as_json_str())
        response = self.__connection.Delete(request)
        self.validate_response(response)

    def check_and_replace(self, doc, condition, _id=None):
        if _id is not None:
            doc.set_id(_id=_id)
        doc_str = OJAIDocumentStore.__get_doc_str(doc=doc)
        str_condition = OJAIDocumentStore.__get_str_condition(
            condition=condition)
        self.__evaluate_doc(doc_str=doc_str, operation_type='REPLACE',
                            condition=str_condition)

    @staticmethod
    def __validate_document(doc_to_insert):
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        if doc_to_insert is None:
            raise InvalidOJAIDocumentError
        if not isinstance(doc_to_insert, OJAIDocument):
            raise IllegalArgumentError(m="Invalid type of the parameter.")

        if '_id' in doc_to_insert.as_dictionary() and isinstance(
                doc_to_insert.as_dictionary()['_id'], (str, unicode)):
            return True

        raise InvalidOJAIDocumentError(m="Invalid OJAI Document")

    @staticmethod
    def __validate_dict(dict_to_insert):
        if not isinstance(dict_to_insert, dict):
            raise TypeError

        if '_id' in dict_to_insert and isinstance(dict_to_insert['_id'],
                                                  (str, unicode)):
            return True

        raise InvalidOJAIDocumentError(m="Invalid dictionary")

    @staticmethod
    def validate_response(response):
        if response.error.err_code == ErrorCode.Value('NO_ERROR'):
            return
        if response.error.err_code == ErrorCode.Value('CLUSTER_NOT_FOUND'):
            raise ClusterNotFoundError(m=response.error.error_message)
        if response.error.err_code == ErrorCode.Value(
                'UNKNOWN_PAYLOAD_ENCODING'):
            raise UnknownPayloadEncodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('PATH_NOT_FOUND'):
            raise PathNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('TABLE_NOT_FOUND'):
            raise StoreNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value(
                'DOCUMENT_ALREADY_EXISTS'):
            raise DocumentAlreadyExistsError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('ENCODING_ERROR'):
            raise EncodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('DECODING_ERROR'):
            raise DecodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('UNKNOWN_ERROR'):
            raise UnknownServerError('Check server logs.')
