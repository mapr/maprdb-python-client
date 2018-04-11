from collections import deque

from ojai.document.DocumentStream import DocumentStream

from mapr.ojai.ojai.OJAIDocument import OJAIDocument


class OJAIDocumentStream(DocumentStream):

    def __init__(self, input_stream=None, query_plan=None):
        # TODO we store documents as list or queue?
        if not isinstance(input_stream, list) or not all(isinstance(n, (OJAIDocument, dict)) for n in input_stream):
            raise TypeError("Input stream must be list of OJAODocuments")
        self.__document_stream = deque(input_stream)
        self.__query_plan = query_plan
        # if list
        # self.__document_stream = input_stream

    def __iter__(self):
        # if deque
        return self
        # if list
        # return iter(self.__document_stream)

    # if deque
    def next(self):
        if self.__document_stream:
            return self.__document_stream.popleft()
        else:
            raise StopIteration

    # TODO this method not needed, __iter__ is build in method in python
    def iterator(self):
        return self.__iter__()

    def close(self):
        raise StopIteration

    def get_query_plan(self):
        return self.__query_plan

    def as_list_of_dictionary(self):
        return map(lambda doc:
                   doc.as_dictionary(),
                   list(self.__document_stream))
        # return list(self.__document_stream)

    @staticmethod
    def new_document_stream(fs, path, field_path_type_map=None, event_delegate=None):
        pass
