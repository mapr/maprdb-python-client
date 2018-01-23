from abc import ABCMeta, abstractmethod


class Value:
    __metaclass__ = ABCMeta

    __TYPE_CODE_NULL = 1
    __TYPE_CODE_BOOLEAN = 2
    __TYPE_CODE_STRING = 3
    __TYPE_CODE_BYTE = 4
    __TYPE_CODE_INT = 5
    __TYPE_CODE_LONG = 6
    __TYPE_CODE_FLOAT = 7
    __TYPE_CODE_DECIMAL = 8
    __TYPE_CODE_DATE = 9
    __TYPE_CODE_TIME = 10
    __TYPE_CODE_TIMESTAMP = 11
    __TYPE_CODE_INTERVAL = 12
    __TYPE_CODE_BINARY = 13
    __TYPE_CODE_MAP = 14
    __TYPE_CODE_ARRAY = 15

    @property
    def type_code_boolean(self):
        return self.__TYPE_CODE_BOOLEAN

    @property
    def type_code_null(self):
        return self.__TYPE_CODE_NULL

    @property
    def type_code_string(self):
        return self.__TYPE_CODE_STRING

    @property
    def type_code_byte(self):
        return self.__TYPE_CODE_BYTE

    @property
    def type_code_int(self):
        return self.__TYPE_CODE_INT

    @property
    def type_code_long(self):
        return self.__TYPE_CODE_LONG

    @property
    def type_code_float(self):
        return self.__TYPE_CODE_FLOAT

    @property
    def type_code_decimal(self):
        return self.__TYPE_CODE_DECIMAL

    @property
    def type_code_date(self):
        return self.__TYPE_CODE_DATE

    @property
    def type_code_time(self):
        return self.__TYPE_CODE_TIME

    @property
    def type_code_timestamp(self):
        return self.__TYPE_CODE_TIMESTAMP

    @property
    def type_code_interval(self):
        return self.__TYPE_CODE_INTERVAL

    @property
    def type_code_binary(self):
        return self.__TYPE_CODE_BINARY

    @property
    def type_code_map(self):
        return self.__TYPE_CODE_MAP

    @property
    def type_code_array(self):
        return self.__TYPE_CODE_ARRAY

    # @staticmethod
    # def is_scalar(value):
    #     return value != Value.type_code_map and value != Value.type_code_array
    #
    # @staticmethod
    # def is_numeric(value):
    #     return Value.type_code_byte <= value <= Value.type_code_decimal


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
class ValueType(object):
    def __init__(self, value_type):
        self.__value = value_type

    NULL = Value.type_code_null

    BOOLEAN = Value.type_code_boolean

    STRING = Value.type_code_string

    BYTE = Value.type_code_byte

    INT = Value.type_code_int

    LONG = Value.type_code_long

    FLOAT = Value.type_code_float

    DECIMAL = Value.type_code_decimal

    DATE = Value.type_code_date

    TIME = Value.type_code_time

    TIMESTAMP = Value.get_timestamp

    INTERVAL = Value.type_code_interval

    BINARY = Value.type_code_binary

    MAP = Value.type_code_map

    ARRAY = Value.type_code_array

    @staticmethod
    def __is_scalar__(value):
        return value != Value.type_code_map and value != Value.type_code_array

    @staticmethod
    def __is_numeric__(value):
        return Value.type_code_byte <= value <= Value.type_code_decimal