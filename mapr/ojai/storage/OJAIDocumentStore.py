from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from past.builtins import *
from past.utils import old_div
import json

from ojai.store.DocumentStore import DocumentStore
from retrying import retry

from mapr.ojai.exceptions.ClusterNotFoundError import ClusterNotFoundError
from mapr.ojai.exceptions.DecodingError import DecodingError
from mapr.ojai.exceptions.DocumentAlreadyExistsError import \
    DocumentAlreadyExistsError
from mapr.ojai.exceptions.DocumentNotFoundError import DocumentNotFoundError
from mapr.ojai.exceptions.EncodingError import EncodingError
from mapr.ojai.exceptions.IllegalArgumentError import IllegalArgumentError
from mapr.ojai.exceptions.IllegalMutationError import IllegalMutationError
from mapr.ojai.exceptions.InvalidOJAIDocumentError import \
    InvalidOJAIDocumentError
from mapr.ojai.exceptions.PathNotFoundError import PathNotFoundError
from mapr.ojai.exceptions.StoreNotFoundError import StoreNotFoundError
from mapr.ojai.exceptions.UnknownPayloadEncodingError import \
    UnknownPayloadEncodingError
from mapr.ojai.exceptions.UnknownServerError import UnknownServerError
from mapr.ojai.ojai import document_utils
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai.OJAIQueryResult import OJAIQueryResult
from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.proto.gen.maprdb_server_pb2 import InsertOrReplaceRequest, \
    PayloadEncoding, FindByIdRequest, ErrorCode, \
    InsertMode, FindRequest, DeleteRequest, UpdateRequest
from mapr.ojai.utils.retry_utils import retry_if_connection_not_established
from mapr.ojai.ojai.OJAITagsBuilder import OJAITagsBuilder
import logging

LOG = logging.getLogger(__name__)
MAX_TIMEOUT = 2147483647


class OJAIDocumentStore(DocumentStore):

    def __init__(self, url, store_path, connection, retry_config):
        self.__url = url
        self.__store_path = store_path
        self.__connection = connection
        self.__retry_config = retry_config
        self.__configure_retry(self.__retry_config)

    def __configure_retry(self, retry_config):
        retry_dec = retry(
            wait_exponential_multiplier=retry_config.wait_exponential_multiplier,
            wait_exponential_max=retry_config.wait_exponential_max,
            stop_max_attempt_number=retry_config.stop_max_attempt_number,
            retry_on_exception=retry_if_connection_not_established
        )
        self.find_by_id = retry_dec(self.find_by_id)
        self.find = retry_dec(self.find)
        self.__evaluate_doc = retry_dec(self.__evaluate_doc)
        self.insert_or_replace = retry_dec(self.insert_or_replace)
        self.delete = retry_dec(self.delete)
        self.insert = retry_dec(self.insert)
        self.replace = retry_dec(self.replace)
        self.check_and_delete = retry_dec(self.check_and_delete)
        self.update = retry_dec(self.update)
        self.check_and_update = retry_dec(self.check_and_update)
        self.check_and_replace = retry_dec(self.check_and_replace)
        self.increment = retry_dec(self.increment)

    @staticmethod
    def __get_str_mutation(mutation):
        from mapr.ojai.document.OJAIDocumentMutation import \
            OJAIDocumentMutation
        if not isinstance(mutation, (OJAIDocumentMutation, dict)):
            raise IllegalArgumentError(
                m='Mutation type must be OJAIDocumentMutation or dict.')
        mutation_with_tags = OJAITagsBuilder().set('mutation',
                                                   mutation.as_dict()
                                                   if isinstance(mutation,
                                                                 OJAIDocumentMutation)
                                                   else mutation).as_dictionary()['mutation']
        return json.dumps(mutation_with_tags,
                          default=document_utils.type_serializer)

    @staticmethod
    def __get_str_condition(condition):
        from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
        if not isinstance(condition, (OJAIQueryCondition, dict)):
            raise IllegalArgumentError(
                m='Condition must be instance of OJAIQueryCondition, dict.')

        condition_with_tags = OJAITagsBuilder().set('condition',
                                                    condition.as_dictionary()
                                                    if isinstance(condition,
                                                                  OJAIQueryCondition)
                                                    else condition).as_dictionary()['condition']
        return json.dumps({'$condition': condition_with_tags},
                          default=document_utils.type_serializer)

    @staticmethod
    def __get_doc_str(doc, _id=None):
        if not isinstance(doc, (OJAIDocument, dict)):
            raise IllegalArgumentError(m="Invalid type of the doc parameter.")
        if isinstance(doc, dict):
            doc = OJAIDocument().from_dict(doc)
        if _id is not None:
            doc.set_id(_id=_id)
        return doc.as_json_str()

    @staticmethod
    def __build_find_by_id_result(response, results_as_document):
        from mapr.ojai.ojai_utils.ojai_document_creator import OJAIDocumentCreator

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
        if not isinstance(_id, basestring):
            raise TypeError

        request = FindByIdRequest(table_path=self.__store_path,
                                  payload_encoding=PayloadEncoding.Value(
                                      'JSON_ENCODING'),
                                  json_document=OJAIDocument().set_id(_id=_id).as_json_str())
        if condition is not None:
            if not isinstance(condition, (OJAIQueryCondition, dict)):
                raise IllegalArgumentError(
                    m='Condition must be instance of OJAIQueryCondition, dict.')
            request.json_condition = json.dumps(condition
                                                if isinstance(condition, dict)
                                                else condition.as_dictionary(),
                                                default=document_utils.type_serializer)
        if field_paths is not None:
            if not isinstance(field_paths, (list, basestring)):
                raise IllegalArgumentError(
                    m='Field paths must be instance of list, str.')
            request.projections[:] = field_paths \
                if isinstance(field_paths, list) \
                else field_paths.split(',')

        LOG.debug('Sending FIND BY ID request to the server. Request body: %s', request)
        if timeout is None:
            response = self.__connection.FindById(request)
        else:
            response = self.__connection.FindById(request, timeout=timeout)
        LOG.debug('Got FIND BY ID response from the server. Response body: %s', response)
        return self.__build_find_by_id_result(response=response,
                                              results_as_document=results_as_document)

    def __get_query_str(self, query=None):
        if query is None:
            query_str = '{}'
        elif isinstance(query, basestring):
            query_str = query
        elif isinstance(query, OJAIQuery):
            query_str = query.to_json_str()
        elif isinstance(query, dict):
            query_str = json.dumps(query,
                                   default=document_utils.type_serializer)
        else:
            raise IllegalArgumentError(
                m="Invalid type of the query parameter.")
        return query_str

    def find(self, query=None, options=None):
        if options is None:
            options = {}
        query_str = self.__get_query_str(query)
        include_query_plan = options.get('ojai.mapr.query.include-query-plan',
                                         False)
        timeout = options.get('ojai.mapr.query.timeout-milliseconds', None)
        if timeout is not None:
            if timeout > MAX_TIMEOUT:
                raise IllegalArgumentError('ojai.mapr.query.'
                                           'timeout-milliseconds'
                                           ' cannot be > {0}.'
                                           .format(MAX_TIMEOUT))
            # Converting timeout from milliseconds to seconds,
            # due to gRPC expect timeout in seconds.
            timeout = old_div(timeout, 1000.0)
        result_as_document = \
            options.get('ojai.mapr.query.result-as-document', False)

        request = FindRequest(table_path=self.__store_path,
                              payload_encoding=PayloadEncoding.Value(
                                  'JSON_ENCODING'),
                              include_query_plan=include_query_plan,
                              json_query=query_str)
        LOG.debug('Sending FIND request to the server. Request body: %s',
                  request)
        if timeout is None:
            response_stream = \
                self.__connection.Find(request)
        else:
            response_stream = \
                self.__connection.Find(request,
                                       timeout=timeout)
        return OJAIQueryResult(document_stream=response_stream,
                               results_as_document=result_as_document,
                               include_query_plan=include_query_plan)

    def __evaluate_doc_stream(self, doc_stream, operation_type):
        LOG.debug('Start sending documents on the server.')
        for doc in doc_stream:
            if isinstance(doc, OJAIDocument):
                self.__validate_dict(doc.as_dictionary())
                doc_str = doc.as_json_str()
            else:
                self.__validate_dict(doc)
                doc_str = OJAIDocument().from_dict(doc).as_json_str()
            self.__evaluate_doc(doc_str=doc_str,
                                operation_type=operation_type)

    def __evaluate_doc(self, doc_str, operation_type, condition=None):
        request = InsertOrReplaceRequest(table_path=self.__store_path,
                                         insert_mode=InsertMode.Value(
                                             operation_type),
                                         payload_encoding=PayloadEncoding
                                         .Value('JSON_ENCODING'),
                                         json_document=doc_str)
        if condition is not None:
            request.json_condition = condition
        LOG.debug('Sending %s request to the server. Request body: %s',
                  operation_type,
                  request)
        response = \
            self.__connection.InsertOrReplace(request)
        LOG.debug('Got %s response from the server. Response body: %s',
                  operation_type,
                  response)
        self.validate_response(response=response)

    def insert_or_replace(self, doc=None, _id=None, field_as_key=None,
                          doc_stream=None):
        if doc_stream is None:
            doc_str = OJAIDocumentStore.__get_doc_str(doc=doc, _id=_id)
            self.__evaluate_doc(doc_str=doc_str,
                                operation_type='INSERT_OR_REPLACE')
        else:
            self.__evaluate_doc_stream(doc_stream, 'INSERT_OR_REPLACE')

    def __evaluate_delete(self, doc_string):
        request = DeleteRequest(table_path=self.__store_path,
                                payload_encoding=PayloadEncoding.Value(
                                    'JSON_ENCODING'),
                                json_document=doc_string)
        LOG.debug('Sending DELETE request to the server. Request body: %s', request)
        response = self.__connection.Delete(request)
        LOG.debug('Got DELETE response from the server. Response body: %s', response)
        self.validate_response(response)

    def __delete_doc_stream(self, doc_stream):
        LOG.debug('Start deleting documents on the server.')
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
        if not isinstance(_id, (basestring, bytearray)):
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

    def insert(self, doc=None, _id=None, field_as_key=None, doc_stream=None):
        if doc_stream is None:
            doc_str = OJAIDocumentStore.__get_doc_str(doc=doc, _id=_id)
            self.__evaluate_doc(doc_str=doc_str, operation_type='INSERT')
        else:
            self.__evaluate_doc_stream(doc_stream, 'INSERT')

    def replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None):
        if doc_stream is None:
            doc_str = OJAIDocumentStore.__get_doc_str(doc=doc, _id=_id)
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
        LOG.debug('Sending UPDATE request to the server. Request body: %s', request)
        response = self.__connection.Update(request)
        LOG.debug('Got UPDATE response from the server. Response body: %s', response)
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
        try:
            self.__execute_update(_id=str_doc,
                                  mutation=str_mutation,
                                  condition=str_condition)
        except DocumentNotFoundError:
            return False
        return True

    def check_and_delete(self, _id, condition):
        str_condition = OJAIDocumentStore.__get_str_condition(
            condition=condition)
        request = DeleteRequest(table_path=self.__store_path,
                                payload_encoding=PayloadEncoding.Value(
                                    'JSON_ENCODING'),
                                json_condition=str_condition,
                                json_document=OJAIDocument().set_id(
                                    _id=_id).as_json_str())
        LOG.debug('Sending CHECK AND DELETE request to the server. Request body: %s', request)
        response = self.__connection.Delete(request)
        LOG.debug('Got CHECK AND DELETE response from the server. Response body: %s', response)
        self.validate_response(response)

    def check_and_replace(self, doc, condition, _id=None):
        if _id is not None:
            doc.set_id(_id=_id)
        doc_str = OJAIDocumentStore.__get_doc_str(doc=doc, _id=_id)
        str_condition = OJAIDocumentStore.__get_str_condition(
            condition=condition)
        try:
            self.__evaluate_doc(doc_str=doc_str, operation_type='REPLACE',
                                condition=str_condition)
        except DocumentNotFoundError:
            return False
        return True

    @staticmethod
    def __validate_document(doc_to_insert):
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        if doc_to_insert is None:
            raise InvalidOJAIDocumentError
        if not isinstance(doc_to_insert, OJAIDocument):
            raise IllegalArgumentError(m="Invalid type of the parameter.")

        if '_id' in doc_to_insert.as_dictionary() and isinstance(
                doc_to_insert.as_dictionary()['_id'], basestring):
            return True

        raise InvalidOJAIDocumentError(m="Invalid OJAI Document")

    @staticmethod
    def __validate_dict(dict_to_insert):
        if not isinstance(dict_to_insert, dict):
            raise TypeError

        if '_id' in dict_to_insert and isinstance(dict_to_insert['_id'],
                                                  basestring):
            return True

        raise InvalidOJAIDocumentError(m="Invalid dictionary")

    @staticmethod
    def validate_response(response):
        if response.error.err_code == ErrorCode.Value('NO_ERROR'):
            return
        if response.error.err_code == ErrorCode.Value('CLUSTER_NOT_FOUND'):
            raise ClusterNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value(
                'UNKNOWN_PAYLOAD_ENCODING'):
            raise UnknownPayloadEncodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('PATH_NOT_FOUND'):
            raise PathNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('DOCUMENT_NOT_FOUND'):
            raise DocumentNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('TABLE_NOT_FOUND'):
            raise StoreNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value(
                'DOCUMENT_ALREADY_EXISTS'):
            raise DocumentAlreadyExistsError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('ENCODING_ERROR'):
            raise EncodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('DECODING_ERROR'):
            raise DecodingError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('PATH_NOT_FOUND'):
            raise PathNotFoundError(m=response.error.error_message)
        elif response.error.err_code == ErrorCode.Value('ILLEGAL_MUTATION'):
            raise IllegalMutationError(m=response.error.error_message)
        else:
            raise UnknownServerError(m=response.error.error_message)
