from abc import ABCMeta, abstractmethod


class DocumentBuilder:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def put(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_float(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_byte(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_byte_array(self, field, value, offset=None, length=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_date(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_time(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_decimal(self, field, value, scale=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_date(self, field, days):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_time(self, field, millis):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_timestamp(self, field, time_millis):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_new_interval(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_map(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_new_map(self, field):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_new_array(self, field):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_null(self, field):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_document(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def put_value_obj(self, field, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def set_array_index(self, index):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add(self, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_boolean(self, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_byte(self, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_long(self, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_float(self, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_byte_array(self, value, offset=None, length=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_document(self, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_value_obj(self, value):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_decimal(self, decimal_value, scale=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_null(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_new_array(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_new_map(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_time(self, millis):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_date(self, days):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_timestamp(self, time_millis):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_interval(self, duration_in_ms):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def end_array(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def add_map(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_document(self):
        raise NotImplementedError("Should have implemented this")
