import decimal
from ojai.o_types.ODate import ODate
from ojai.o_types.OInterval import OInterval
from ojai.o_types.OTime import OTime
from ojai.o_types.OTimestamp import OTimestamp

from mapr.ojai.ojai.OJAIList import OJAIList
from mapr.ojai.ojai.document_utils import parse_field_path, merge_two_dicts


class OJAITagsBuilder:

    def __init__(self):
        self.__internal_dict = {}

    def clear(self):
        self.__internal_dict = {}

    def set(self, field_path, value, off=None, length=None):
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        if field_path == '_id' and isinstance(value, (unicode, str)):
            self.__internal_dict[field_path] = value
        elif isinstance(value, OJAIDocument):
            self.__set_document(field_path=field_path, value=value)
        elif value is None:
            self.__set_none(field_path=field_path)
        else:
            self.__set_dispatcher(field_path=field_path, value=value)

        return self

    def __set_str(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value))

    def __set_boolean(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value))

    def __set_long(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value,
                                                                oja_type='$numberLong'))

    def __set_float(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value,
                                                                oja_type='$numberFloat'))

    def __set_decimal(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value.to_eng_string(),
                                                                oja_type='$decimal'))

    def __set_time(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value.time_to_str(),
                                                                oja_type='$time'))

    def __set_date(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value.to_date_str(),
                                                                oja_type='$dateDay'))

    def __set_timestamp(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value.__str__(),
                                                                oja_type='$date'))

    def __set_interval(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value.time_duration,
                                                                oja_type='$interval'))

    def __set_byte_array(self, field_path, value, offset=None, length=None):
        # TODO ISO-8859-1 or utf-8 ?
        to_str = value.decode('ISO-8859-1')
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=to_str,
                                                                oja_type='$binary'))

    def __set_dict(self, field_path, value):
        from mapr.ojai.ojai.OJAIDict import OJAIDict
        value = OJAIDict.parse_dict(value, tags=True)
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value))

    def __set_document(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value.as_dictionary()))

    def __set_array(self, field_path, value):
        list_value = OJAIList.set_list(value=value, tags=True)
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=list_value))

    def __set_none(self, field_path):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=None))

    __dispatcher = {
        str: __set_str,
        unicode: __set_str,
        bool: __set_boolean,
        int: __set_long,
        long: __set_long,
        float: __set_float,
        OTime: __set_time,
        OTimestamp: __set_timestamp,
        ODate: __set_date,
        OInterval: __set_interval,
        list: __set_array,
        dict: __set_dict,
        bytearray: __set_byte_array,
        decimal.Decimal: __set_decimal,
        None: __set_none
    }

    def __set_dispatcher(self, field_path, value):
        t = type(value)
        f = OJAITagsBuilder.__dispatcher[t]
        f(self, field_path, value)

    def as_dictionary(self):
        return self.__internal_dict
