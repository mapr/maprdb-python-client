from abc import ABCMeta, abstractmethod


class DocumentListener:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def document_arrived(self, doc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def failed(self, exception):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def eos(self):
        raise NotImplementedError("Should have implemented this")