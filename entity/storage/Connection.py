from abc import ABCMeta, abstractmethod


class Connection:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_store(self, store_name, options=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_value_buffer(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_document(self, json_string=None, json_map=None, obj=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_document_builder(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_mutation(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_condition(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_query(self, query_json=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_driver(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def close(self):
        raise NotImplementedError("Should have implemented this")
