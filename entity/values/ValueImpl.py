from Value import Value, ValueType
from entity.o_types.OInterval import OInterval


class ValueImpl(Value):

    def __init__(self, value_type=None, json_value=None, obj_value=None):
        self.value_type = value_type
        self.json_value = json_value
        self.obj_value = obj_value
        self.key = None

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def check_type(self, value_type):
        if self.value_type != value_type:
            raise TypeError("Value is of type " + self.value_type + " but requested type is " + value_type)
        return

    def set_prim_value(self, value):
        self.json_value = value

    def set_obj_value(self, value):
        # TODO added chat that value is object. Which objects acceptable?
        #  Only ValueType objects? ValueType object don't store as enum in python
        self.obj_value = value

    def get_obj(self):
        switcher = {
            1: self.obj_value,
            2: self.get_boolean(),
            3: self.obj_value,
            4: self.get_byte(),
            5: self.get_int(),
            6: self.get_long(),
            7: self.get_float(),
            8: self.obj_value,
            9: self.get_date(),
            10: self.get_time(),
            11: self.get_timestamp(),
            12: self.get_interval(),
            13: self.obj_value,
            14: self,
            15: self
        }
        return switcher.get(self.value_type, TypeError("Invalid type " + self.value_type))

    def get_date(self):
        self.check_type(ValueType.DATE)
        if self.obj_value is None:
            # TODO implement ODate class
            pass

    def get_map(self):
        self.check_type(ValueType.MAP)
        # TODO added get_map implementation after JSONDocument will done
        pass

    def get_time_as_int(self):
        return int(self.json_value)

    def get_type(self):
        return self.value_type

    def get_interval(self):
        self.check_type(ValueType.INTERVAL)
        if self.obj_value is None:
            # TODO implement OTimeStamp class
            # self.obj_value = OInterval(self.json_value)
            pass
        return self.obj_value

    def get_list(self):
        self.check_type(ValueType.ARRAY)
        # TODO added get_map implementation after JSONList will done
        pass

    def get_byte(self):
        switcher = {
            ValueType.BYTE: self.int_to_byte(self.json_value),
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
            # TODO implement OTime class
            pass

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
            # TODO implement OTimeStamp class
            pass

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

    # TODO Implement method which convert int to byte
    def int_to_byte(self, value):
        pass

    # TODO Implement method which convert byte to int
    def byte_to_int(self, value):
        pass

    # TODO check get_binary and how we can implement it

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
