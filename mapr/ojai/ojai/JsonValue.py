from __future__ import division

from decimal import Decimal
from ojai.values.Value import Value, ValueType

from mapr.ojai.exceptions import UnsupportedConstructorException
from mapr.ojai.ojai.OJAIList import OJAIList
from mapr.ojai.o_types.ODate import ODate
from mapr.ojai.o_types.OInterval import OInterval
from mapr.ojai.o_types.OTime import OTime
from mapr.ojai.o_types.OTimestamp import OTimestamp
from struct import *


class JsonValue(Value):
    def __init__(self, value_type=None, json_value=None, obj_value=None, bool_value=None):
        # type in ValueType enum
        self.value_type = value_type
        # if bool_value was set into params - json_value will parsed from it
        if bool_value is not None and isinstance(bool_value, bool) and value_type is not None:
            self.json_value = 1 if bool_value else 0
        elif json_value is not None:
            self.json_value = json_value
        else:
            self.json_value = None
        # object
        if value_type is None or obj_value is None:
            raise UnsupportedConstructorException
        self.obj_value = obj_value
        self.key = None

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def check_type(self, value_type):
        if self.value_type != value_type:
            raise TypeError("Value is of type " + self.value_type + " but requested type is " + value_type)
        return True

    def set_prim_value(self, value):
        self.json_value = value

    def set_obj_value(self, value):
        # TODO added check that value is object. Which objects acceptable?
        #  Only ValueType objects?
        self.obj_value = value

    def get_obj(self):
        switcher = {
            ValueType.NULL: lambda: self.obj_value,
            ValueType.BOOLEAN: lambda: self.get_boolean,
            ValueType.STRING: lambda: self.obj_value,
            ValueType.BYTE: lambda: self.get_byte(),
            ValueType.INT: lambda: self.get_int(),
            ValueType.LONG: lambda: self.get_long(),
            ValueType.FLOAT: lambda: self.get_float(),
            ValueType.DECIMAL: lambda: self.obj_value,
            ValueType.DATE: lambda: self.get_date(),
            ValueType.TIME: lambda: self.get_time(),
            ValueType.TIMESTAMP: lambda: self.get_timestamp(),
            ValueType.INTERVAL: lambda: self.get_interval(),
            ValueType.BINARY: lambda: self.obj_value,
            ValueType.ARRAY: lambda: self,
            ValueType.DICTIONARY: lambda: self
        }
        return switcher.get(self.value_type, TypeError("Invalid type " + str(self.value_type)))()

    def get_date(self):
        self.check_type(ValueType.DATE)
        if self.obj_value is None:
            self.obj_value = ODate.from_days_since_epoch(self.json_value)
        return self.obj_value

    def get_dictionary(self):
        self.check_type(ValueType.DICTIONARY)
        # TODO added get_map implementation after JSONDocument will done
        # TODO Test it
        from mapr.ojai.ojai import OJAIDocument
        doc = OJAIDocument(json_value=self)
        return doc

    def get_time_as_int(self):
        return int(self.json_value)

    def get_type(self):
        return self.value_type

    def get_interval(self):
        self.check_type(ValueType.INTERVAL)
        if self.obj_value is None:
            self.obj_value = OInterval(self.json_value)
        return self.obj_value

    def get_list(self):
        self.check_type(ValueType.ARRAY)
        # TODO added get_map implementation after JSONList will done
        # TODO TEST IT
        json_list = OJAIList(json_value=self)
        return json_list

    def get_byte(self):
        # switcher = {
        #     ValueType.BYTE: lambda: self.int_to_byte(self.json_value),
        #     ValueType.INT: lambda: self.get_int,
        #     ValueType.LONG: lambda: self.get_long,
        #     ValueType.FLOAT: lambda: self.get_float,
        #     ValueType.DECIMAL: lambda: self.get_decimal
        # }
        #
        if self.value_type is ValueType.BYTE:
            return self.int_to_byte(self.json_value)
        elif self.value_type is ValueType.INT:
            return self.get_int()
        elif self.value_type is ValueType.LONG:
            return self.get_long()
        elif self.value_type is ValueType.FLOAT:
            return self.get_float()
        elif self.value_type is ValueType.DECIMAL:
            return self.get_decimal()
        else:
            return TypeError("Expected a numeric type, found: " + self.value_type)
        # return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))

    def get_time(self):
        self.check_type(ValueType.TIME)
        if self.obj_value is None:
            self.obj_value = OTime.from_millis_of_day(millis_of_day=self.json_value)
        return self.obj_value

    def get_binary(self):
        # TODO implement it
        pass

    def get_long(self):
        # switcher = {
        #     ValueType.LONG: self.json_value,
        #     ValueType.BYTE: long(self.byte_to_int(self.get_byte())),
        #     ValueType.INT: long(self.get_int()),
        #     ValueType.FLOAT: long(self.get_float()),
        #     ValueType.DECIMAL: self.get_decimal().__long__()
        # }
        # return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))
        if self.value_type is ValueType.LONG:
            return self.json_value
        elif self.value_type is ValueType.BYTE:
            return long(self.byte_to_int(self.get_byte()))
        elif self.value_type is ValueType.INT:
            return long(self.get_int())
        elif self.value_type is ValueType.FLOAT:
            return long(self.get_float())
        elif self.value_type is ValueType.DECIMAL:
            return self.get_decimal().__long__()
        else:
            return TypeError("Expected a numeric type, found: " + self.value_type)

    def get_int(self):
        # switcher = {
        #     ValueType.INT: int(self.json_value),
        #     ValueType.BYTE: self.byte_to_int(self.get_byte()),
        #     ValueType.LONG: int(self.get_long()),
        #     ValueType.FLOAT: int(self.get_float()),
        #     ValueType.DECIMAL: self.get_decimal().__int__()
        # }
        if self.value_type is ValueType.INT:
            return int(self.json_value)
        elif self.value_type is ValueType.BYTE:
            return self.byte_to_int(self.get_byte())
        elif self.value_type is ValueType.LONG:
            return int(self.get_long())
        elif self.value_type is ValueType.FLOAT:
            return int(self.get_float())
        elif self.value_type is ValueType.DECIMAL:
            self.get_decimal().__int__()
        else:
            return TypeError("Expected a numeric type, found: " + self.value_type)
        # return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))

    def get_date_as_int(self):
        return int(self.json_value)

    def get_boolean(self):
        self.check_type(ValueType.BOOLEAN)
        return self.json_value != 0

    def get_timestamp(self):
        self.check_type(ValueType.TIMESTAMP)
        if self.obj_value is None:
            self.obj_value = OTimestamp(millis_since_epoch=self.json_value)
        return self.obj_value

    def get_decimal(self):
        switcher = {
            ValueType.DECIMAL: Decimal(self.obj_value),
            ValueType.FLOAT: Decimal(self.get_float()),
            ValueType.BYTE: Decimal(self.get_byte()),
            ValueType.INT: Decimal(self.get_int()),
            ValueType.LONG: Decimal(self.get_long())
        }
        return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))

    def get_string(self):
        self.check_type(ValueType.STRING)
        return str(self.obj_value)

    def get_float(self):
        # switcher = {
        #     ValueType.FLOAT: float(self.json_value),
        #     ValueType.BYTE: self.get_byte(),
        #     ValueType.INT: float(self.get_int()),
        #     ValueType.LONG: float(self.get_long()),
        #     ValueType.DECIMAL: Decimal(self.get_decimal()).__float__()
        # }
        if self.value_type is ValueType.FLOAT:
            return float(self.json_value)
        elif self.value_type is ValueType.BYTE:
            return self.get_byte()
        elif self.value_type is ValueType.INT:
            return float(self.get_int())
        elif self.value_type is ValueType.LONG:
            return float(self.get_long())
        elif self.value_type is ValueType.DECIMAL:
            return self.get_decimal().__float__()
        else:
            return TypeError("Expected a numeric type, found: " + self.value_type)
        # return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))

    def get_interval_as_long(self):
        return long(self.json_value)

    def get_timestamp_as_long(self):
        return self.json_value

    @staticmethod
    def int_to_byte(value):
        result = pack('h', value)
        return result

    @staticmethod
    def byte_to_int(value):
        result = unpack('h', value)[0]
        return result

    # TODO check is shallowCopy method required
    def shallow_copy(self):
        pass

    # this OJAI object serialized as JSON string using the default options
    # TODO options param required JsonOptions implementation
    def as_json_string(self, options=None):
        # TODO returns org.ojai.ojai.JSON.toJsonString implementation.
        pass

    # TODO required as_json_string method!
    # def __str__(self):
    #     return self.as_json_string()

    def __eq__(self, other):
        if other is None:
            return self.value_type is ValueType.NULL
        elif isinstance(self, type(other)):
            if self.value_type is not other.get_type():
                return False
            if self.value_type is any([ValueType.BOOLEAN, ValueType.BYTE, ValueType.INT, ValueType.LONG,
                                      ValueType.FLOAT, ValueType.DECIMAL, ValueType.DATE, ValueType.INTERVAL,
                                      ValueType.TIME, ValueType.TIMESTAMP]):
                return self.json_value == other.json_value
            elif self.value_type is ValueType.NULL:
                return self.obj_value is None and other.obj_value is None
            # elif self.value_type is any([ValueType.BINARY, ValueType.DECIMAL,
            #                             ValueType.STRING, ValueType.DICTIONARY, ValueType.ARRAY]):
            elif self.value_type is ValueType.BINARY or self.value_type is ValueType.DECIMAL \
                    or self.value_type is ValueType.STRING or self.value_type is ValueType.DICTIONARY \
                    or self.value_type is ValueType.ARRAY:
                # TODO check it with Aditya
                a = self.obj_value
                b = other.obj_value
                # return self.__eq__(other=other.get_obj())
                return self.obj_value == other.obj_value
        elif isinstance(other, str) and self.value_type != ValueType.BYTE:
            return self.obj_value == other
        elif isinstance(other, bytes):
            # todo check for byte
            return other.__eq__(self.get_byte())
        elif isinstance(other, bool):
            return other == self.get_boolean()
        elif isinstance(other, float):
            b = self.get_float()
            return other == b
        elif isinstance(other, int):
            return other == self.get_int()
        elif isinstance(other, long):
            return other == self.get_long()
        elif isinstance(other, Decimal):
            return other == self.get_decimal()
        elif isinstance(other, ODate):
            date_as_long = other.to_days_since_epoch()
            return self.json_value == date_as_long
        elif isinstance(other, OTime):
            time_as_long = other.to_time_in_millis()
            return self.json_value == time_as_long
        elif isinstance(other, OTimestamp):
            timestamp_as_long = other.get_millis()
            return self.json_value == timestamp_as_long
        elif isinstance(other, OInterval):
            return other.__eq__(self.get_interval())
        elif isinstance(other, bytearray):
            return other.__eq__(self.get_binary())
        elif isinstance(other, dict):
            return self.obj_value.__eq__(other)
        elif isinstance(other, list):
            return self.obj_value.__eq__(other)
        elif isinstance(other, JsonValue):
            return self.__eq__(other).get_obj()
        else:
            return False
