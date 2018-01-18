from abc import ABCMeta, abstractmethod


class Document:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def set_id(self, _id):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_id(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_id_string(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_id_binary(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def size(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def empty(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set(self, field_path, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_array(self, field_path, values):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_null(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def delete(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_string(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_boolean(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_byte(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_short(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_int(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_long(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_float(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_double(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_decimal(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_time(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_date(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_timestamp(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_binary(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_interval(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_value(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_map(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_list(self, field_path):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def as_reader(self, field_path=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def as_map(self):
        raise NotImplementedError("Should have implemented this")
