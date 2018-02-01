from entity.values.Value import Value, ValueType
from entity.json.JsonList import JsonList
from entity.o_types.ODate import ODate
from entity.o_types.OInterval import OInterval
from entity.o_types.OTime import OTime
from entity.o_types.OTimestamp import OTimestamp
from struct import *


class JsonValue(Value):

    def __init__(self, value_type=None, json_value=None, obj_value=None, bool_value=None):
        # type in ValueType enum
        self.value_type = value_type
        # if bool_value was set into params - json_value will parsed from it
        if bool_value is not None and isinstance(bool_value, bool) and value_type is not None:
            self.json_value = 1 if bool_value else 0
        elif json_value is not None:
            self.json_value = long(json_value)
        else:
            self.json_value = None
        # object
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
        # TODO added chat that value is object. Which objects acceptable?
        #  Only ValueType objects? ValueType object don't store as enum in python
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
            ValueType.MAP: lambda: self
        }
        return switcher.get(self.value_type, TypeError("Invalid type " + str(self.value_type)))()

    def get_date(self):
        self.check_type(ValueType.DATE)
        if self.obj_value is None:
            self.obj_value = ODate.from_days_since_epoch(self.json_value)
        return self.obj_value

    def get_map(self):
        self.check_type(ValueType.MAP)
        # TODO added get_map implementation after JSONDocument will done
        # TODO Test it
        from entity.json.JsonDocument import JsonDocument
        doc = JsonDocument(json_value=self)
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
        json_list = JsonList(json_value=self)
        return json_list

    def get_byte(self):
        switcher = {
            ValueType.BYTE: self.int_to_byte(self.json_value, str(self.json_value).__len__()),
            ValueType.INT: self.get_int(),
            ValueType.LONG: self.get_long(),
            ValueType.FLOAT: self.get_float(),
            # TODO convert decimal to byte
            ValueType.DECIMAL: self.get_decimal()
        }
        return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))

    def get_time(self):
        self.check_type(ValueType.TIME)
        if self.obj_value is None:
            self.obj_value = OTime.from_millis_of_day(millis_of_day=self.json_value)
        return self.obj_value

    def get_long(self):
        switcher = {
            ValueType.LONG: self.json_value,
            ValueType.BYTE: self.get_byte(),
            ValueType.INT: self.get_int(),
            ValueType.FLOAT: long(self.get_float()),
            # TODO convert decimal to long
            ValueType.DECIMAL: long(self.get_decimal())
        }
        return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))

    def get_int(self):
        switcher = {
            ValueType.INT: self.byte_to_int(self.json_value),
            ValueType.BYTE: self.get_byte(),
            ValueType.FLOAT: int(self.get_float()),
            # TODO convert decimal to int
            ValueType.DECIMAL: int(self.get_decimal())
        }
        return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))

    def as_reader(self):
        # TODO required JsonDOMDocumentReader implementation
        pass

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
        # TODO check and implement get_decimal like java BigDecimal
        pass

    def get_string(self):
        self.check_type(ValueType.STRING)
        return str(self.obj_value)

    def get_float(self):
        switcher = {
            # TODO check how to convert long to float
            ValueType.FLOAT: float(self.json_value),
            ValueType.BYTE: self.get_byte(),
            ValueType.INT: float(self.get_int()),
            ValueType.LONG: float(self.get_long()),
            # TODO convert decimal to float
            ValueType.DECIMAL: int(self.get_decimal())
        }
        return switcher.get(self.value_type, TypeError("Expected a numeric type, found: " + self.value_type))

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
        # TODO returns org.ojai.json.JSON.toJsonString implementation.
        pass

    # TODO required as_json_string method!
    # def __str__(self):
    #     return self.as_json_string()

    # TODO check eq impl
    # def __eq__(self, o):
    #     return super(ValueImpl, self).__eq__(o)
