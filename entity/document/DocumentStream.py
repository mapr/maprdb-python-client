from abc import ABCMeta, abstractmethod


class DocumentStream:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def stream_to(self, doc_listener):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def iterator(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def document_readers(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def close(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_query_plan(self):
        raise NotImplementedError("Should have implemented this")