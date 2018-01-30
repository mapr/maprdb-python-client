from abc import ABCMeta, abstractmethod


class DocumentStream:
    """ A stream of documents.
        Implements Iterable<Document> but only one call is allows to iterator()
        or readerIterator(). Only one of these iterators can be retrieved
        from the stream."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def stream_to(self, doc_listener):
        """Streams all the documents in this {@code DocumentStream} to the specified
        listener.
        doc_listener : a DocumentListener which is notified of JsonDocuments as they arrive"""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def iterator(self):
        """Returns an iterator over a set of JsonDocument"""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def document_readers(self):
        """Returns an Iterable over a set of DocumentReader."""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def close(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_query_plan(self):
        raise NotImplementedError("Should have implemented this")