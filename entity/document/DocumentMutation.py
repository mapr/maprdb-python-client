from abc import ABCMeta, abstractmethod


class DocumentMutation:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def empty(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_null(self, path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set(self, path, value=None, doc=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_collection(self, path, collection):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_null(self, path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def append(self, path, value, offset=None, len=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def merge(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment(self, path, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def decrement(self, path, dec):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def delete(self, path):
        raise NotImplementedError("Should have implemented this")

