from abc import ABCMeta, abstractmethod


class Value:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

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

        INTERVAL = Value.type_code_interval

        BINARY = Value.type_code_binary

        MAP = Value.type_code_map

        ARRAY = Value.type_code_array

        @staticmethod
        def __is_scalar__(value):
            return value != Value.ValueType.MAP and value != Value.ValueType.ARRAY

        @staticmethod
        def __is_numeric__(value):
            return Value.ValueType.BYTE <= value <= Value.ValueType.DECIMAL







