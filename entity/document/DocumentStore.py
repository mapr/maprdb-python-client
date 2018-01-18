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
    def find_by_id(self, _id, field_paths=None, condition=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def find(self, query=None, field_paths=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def find_query(self, query=None, field_paths=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def insert_or_replace(self, doc, _id=None, field_as_key=None, doc_stream=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def update(self, _id, mutation):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def delete(self, _id=None, doc=None, field_as_key=None, doc_stream=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def insert(self, _id=None, doc=None, field_as_key=None, doc_stream=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def insert(self, _id=None, doc=None, field_as_key=None, doc_stream=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment(self, _id, field, inc):
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