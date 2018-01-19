from abc import ABCMeta, abstractmethod


class DocumentStore:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def is_read_only(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def flush(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def begin_tracking_writes(self, previous_writes_context=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def end_tracking_writes(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def clear_tracked_writes(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def find_by_id_value_obj(self, _id, field_paths=None, condition=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def find_by_id_string(self, _id, field_paths=None, condition=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def find_by_id(self, _id, field_paths=None, condition=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def find(self, query=None, field_paths=None, condition=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def find_query(self, query):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def find_query_string(self, query):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def insert_or_replace(self, doc, _id=None, field_as_key=None, doc_stream=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def insert_or_replace_document_stream(self, doc_stream, _id=None, field_as_key=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def update(self, _id, mutation):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def delete_by_id(self, _id):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def delete_document(self, doc, field_as_key=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def delete_document_stream(self, doc_stream, field_as_key=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def insert_document_with_id(self, _id, document):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def insert_document(self, document, field_as_key=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def insert_document_stream(self, document_stream, field_as_key=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def replace_document_with_id(self, _id, document):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def replace_document(self, document, field_as_key=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def replace_document_stream(self, document_stream, field_as_key=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment(self, _id, field, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment_int(self, _id, field, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment_float(self, _id, field, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment_decimal(self, _id, field, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment_byte(self, _id, field, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def check_and_mutate(self, _id, query_condition, mutation):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def check_and_delete(self, _id, condition):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def check_and_replace(self, _id, condition, doc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def close(self):
        raise NotImplementedError("Should have implemented this")