from ojai.document.DocumentStream import DocumentStream


class JsonDocumentStream(DocumentStream):

    __input_stream = None
    __json_parser = None
    __read_started = None
    __iterator_opened = None

    __field_path_type_map = None
    __event_delegate = None

    def __init__(self, input_stream=None, field_path_type_map=None, event_delegate=None):
        pass

    def stream_to(self, doc_listener):
        pass

    def iterator(self):
        pass

    def document_readers(self):
        pass

    def close(self):
        pass

    def get_query_plan(self):
        pass

    @staticmethod
    def new_document_stream(fs, path, field_path_type_map=None, event_delegate=None):
        pass
