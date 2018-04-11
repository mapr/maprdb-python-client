from collections import deque

from ojai.document.DocumentStream import DocumentStream

from mapr.ojai.exceptions.InvalidStreamResponseError import InvalidStreamResponseError
from mapr.ojai.exceptions.UnknownServerError import UnknownServerError
from mapr.ojai.ojai.OJAIDocument import OJAIDocument


class OJAIDocumentStream(DocumentStream):

    def __init__(self, input_stream, results_as_document=False):
        self.__results_as_document = results_as_document
        self.__input_stream = iter(input_stream)

    @staticmethod
    def __parse_find_response(response):
        from mapr.ojai.ojai.OJAIDocumentStore import OJAIDocumentStore
        OJAIDocumentStore.validate_response(response)
        response_type = response.type
        from mapr.ojai.proto.gen.maprdb_server_pb2 import FindResponseType
        if response_type == FindResponseType.Value('RESULT_DOCUMENT'):
            return response.json_response
        else:
            raise InvalidStreamResponseError('Invalid stream response.')

    def __iter__(self):
        return self

    def next(self):
        from mapr.ojai.ojai.OJAIDocumentCreator import OJAIDocumentCreator
        doc_response = None
        for response in self.__input_stream:
            doc_response = OJAIDocumentCreator.create_document(self.__parse_find_response(response))
            break
        if doc_response is None:
            raise StopIteration
        return doc_response if self.__results_as_document else doc_response.as_dictionary()

    def iterator(self):
        return self.__iter__()

    def close(self):
        raise StopIteration

    @staticmethod
    def new_document_stream(fs, path, field_path_type_map=None, event_delegate=None):
        pass


