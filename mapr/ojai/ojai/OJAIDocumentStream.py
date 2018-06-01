from collections import deque

from grpc._channel import _Rendezvous
from ojai.DocumentStream import DocumentStream

from mapr.ojai.exceptions.InvalidStreamResponseError import InvalidStreamResponseError
from mapr.ojai.ojai_utils.ojai_document_creator import OJAIDocumentCreator


class OJAIDocumentStream(DocumentStream):

    def __init__(self, input_stream, results_as_document=False, init_cache=None):
        if init_cache is None or not isinstance(init_cache, deque):
            init_cache = deque()
        self.__results_as_document = results_as_document
        self.__input_stream = iter(input_stream)
        self.__init_cache = init_cache

    @staticmethod
    def parse_find_response(response):
        from mapr.ojai.storage.OJAIDocumentStore import OJAIDocumentStore
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
        if not self.__init_cache:
            self.__fill_cache()
        doc_response = OJAIDocumentCreator\
            .create_document(self.__init_cache.popleft())
        return doc_response if self.__results_as_document else doc_response.as_dictionary()

    def __fill_cache(self):
        try:
            for _ in range(10):
                self.__init_cache.append(OJAIDocumentStream.
                                         parse_find_response(self.__input_stream.next()))
        except _Rendezvous:
            # TODO check code, state before raise!!!
            from mapr.ojai.exceptions.ConnectionLostError import ConnectionLostError
            raise ConnectionLostError(m="Connection lost during operation.")

    def iterator(self):
        return self.__iter__()

    def close(self):
        raise StopIteration

