from abc import ABCMeta, abstractmethod
from aenum import Enum


class Value:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_type(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_byte(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_int(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_long(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_float(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_decimal(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_boolean(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_string(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_timestamp(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_timestamp_as_long(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_date(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_date_as_int(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_time(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_time_as_int(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_interval(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_interval_as_long(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_map(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_list(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_obj(self):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def as_reader(self):
        raise NotImplementedError("Should have implemented this")

    # TODO investigate is we can add binary analog (java.nia.ByteBuffer)
    # @abstractmethod
    # def get_binary(self):
    #     raise NotImplementedError("Should have implemented this")


# TODO Python2 doesn't have enum. Impelement method for convert ValueType numeric field to string like 2 -> "BOOLEAN"
class ValueType(Enum):
    # NULL = Value.type_code_null
    NULL = 1

    # BOOLEAN = Value.type_code_boolean
    BOOLEAN = 2

    # STRING = Value.type_code_string
    STRING = 3

    # BYTE = Value.type_code_byte
    BYTE = 4

    # INT = Value.type_code_int
    INT = 5

    # LONG = Value.type_code_long
    LONG = 6

    # FLOAT = Value.type_code_float
    FLOAT = 7

    # DECIMAL = Value.type_code_decimal
    DECIMAL = 8

    # DATE = Value.type_code_date
    DATE = 9

    # TIME = Value.type_code_time
    TIME = 10

    # TIMESTAMP = Value.get_timestamp
    TIMESTAMP = 11

    # INTERVAL = Value.type_code_interval
    INTERVAL = 12

    # BINARY = Value.type_code_binary
    BINARY = 13

    # MAP = Value.type_code_map
    MAP = 14

    # ARRAY = Value.type_code_array
    ARRAY = 15

    @staticmethod
    def __check_value(value_type):
        value_dict = {ValueType.NULL: 1, ValueType.BOOLEAN: 2, ValueType.STRING: 3, ValueType.BYTE: 4, ValueType.INT: 5,
                      ValueType.LONG: 6, ValueType.FLOAT: 7, ValueType.DECIMAL: 8, ValueType.DATE: 9,
                      ValueType.TIME: 10, ValueType.TIMESTAMP: 11, ValueType.INTERVAL: 12,
                      ValueType.BINARY: 13, ValueType.MAP: 14, ValueType.ARRAY: 15}
        return value_dict[value_type]

    @staticmethod
    def is_scalar(value):
        return ValueType.__check_value(value) != ValueType.__check_value(ValueType.MAP)\
               and ValueType.__check_value(value) != ValueType.__check_value(ValueType.ARRAY)

    @staticmethod
    def is_numeric(value):
        return ValueType.__check_value(ValueType.BYTE) <= ValueType.__check_value(value)\
               <= ValueType.__check_value(ValueType.DECIMAL)
