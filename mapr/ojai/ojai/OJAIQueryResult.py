from ojai.store.QueryResult import QueryResult

from mapr.ojai.exceptions.InvalidStreamResponseError import InvalidStreamResponseError
from mapr.ojai.exceptions.UnknownServerError import UnknownServerError
from mapr.ojai.ojai.OJAIDocumentStream import OJAIDocumentStream
from mapr.ojai.proto.gen.maprdb_server_pb2 import FindResponseType


class OJAIQueryResult(QueryResult):

    def __init__(self, document_stream, results_as_document=False, include_query_plan=False):
        self.__query_plan = None
        self.__doc_stream = document_stream
        self.__include_query_plan = include_query_plan
        self.__results_as_document = results_as_document
        if self.__include_query_plan:
            for response in self.__doc_stream:
                json_response = self.__parse_find_response(response)
                self.__query_plan = json_response
                break

    def __parse_find_response(self, response):
        from mapr.ojai.ojai.OJAIDocumentStore import OJAIDocumentStore
        OJAIDocumentStore.validate_response(response)
        response_type = response.type
        if response_type == FindResponseType.Value('UNKNOWN_TYPE'):
            raise UnknownServerError('Unknown response type.')
        elif response_type == FindResponseType.Value('RESULT_DOCUMENT'):
            return response.json_response
        elif response_type == FindResponseType.Value('QUERY_PLAN'):
            if self.__include_query_plan:
                self.__include_query_plan = False
                return response.json_response
            else:
                raise InvalidStreamResponseError("Invalid response type. Query plan shouldn't be included in response.")
        else:
            raise UnknownServerError('Check server logs.')

    def get_query_plan(self):
        return self.__query_plan

    def __iter__(self):
        return OJAIDocumentStream(input_stream=self.__doc_stream, results_as_document=self.__results_as_document)

