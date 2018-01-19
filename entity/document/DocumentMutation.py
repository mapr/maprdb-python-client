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
    def set(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_string(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_boolean(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_byte(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_long(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_float(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_date(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_time(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_timestamp(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_interval(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_list(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_map(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_document(self, path, doc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_value_obj(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_null(self, path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_value_obj(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_boolean(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_byte(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_long(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_float(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_string(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_decimal(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_date(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_time(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_timestamp(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_interval(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_list(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_map(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_or_replace_doc(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def append(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def append_list(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def append_string(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def append_byte_array(self, path, value, offset=None, length=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def merge(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def merge_document(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def merge_map(self, path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment(self, path, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment(self, path, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment_float(self, path, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment_byte(self, path, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def increment_decimal(self, path, inc):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def decrement(self, path, dec):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def decrement(self, path, dec):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def decrement_float(self, path, dec):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def decrement_byte(self, path, dec):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def decrement_decimal(self, path, dec):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def delete(self, path):
        raise NotImplementedError("Should have implemented this")

