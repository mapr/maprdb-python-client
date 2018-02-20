from ojai.document.DocumentStore import DocumentStore


class JsonDocumentStore(DocumentStore):

    def __init__(self, is_ready_only):
        self.read_only = is_ready_only

    def is_read_only(self):
        if self.read_only is not None:
            return self.read_only
        else:
            # TODO check it to the server via grpc
            pass

    def flush(self):
        pass

    def find_by_id(self, _id, field_paths=None, condition=None):
        pass

    def find(self, query=None, field_paths=None, condition=None, query_string=None):
        pass

    def insert_or_replace(self, doc=None, _id=None, field_as_key=None, doc_stream=None, json_dictionary=None):
        pass

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
