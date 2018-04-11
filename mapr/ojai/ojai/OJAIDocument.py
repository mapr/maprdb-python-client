import json
import re
from copy import deepcopy

import decimal
from ojai.document.Document import Document

from ojai.o_types.ODate import ODate
from ojai.o_types.OInterval import OInterval
from ojai.o_types.OTime import OTime
from ojai.o_types.OTimestamp import OTimestamp
from mapr.ojai.ojai.OJAIDict import OJAIDict
from mapr.ojai.ojai.OJAIList import OJAIList
from mapr.ojai.ojai.document_utils import merge_two_dicts, parse_field_path, replacer


class OJAIDocument(Document):

    # Not needed?
    def get_byte(self, field_path):
        pass

    __json_stream_document_reader = None
    __regex = re.compile(r"""(["']).*?\1|(?P<dot>\.)""")

    def __init__(self, json_value=None):
        self.__internal_dict = {}
        self.json_value = json_value

    def set_id(self, _id):
        """Set _id field into the Document. _id field required for each document in MapR-DB
        :param _id: type should be binary or str"""
        if not isinstance(_id, (unicode, str)):
            raise TypeError
        self.set(field_path="_id", value=_id)
        return self

    def get_id(self):
        return self.__internal_dict['_id']

    def get_id_binary(self):
        raise NotImplementedError

    def size(self):
        return len(self.__internal_dict)

    def empty(self):
        return self.size() == 0

    def clear(self):
        self.__internal_dict = {}

    def get_id_str(self):
        return str(self.__internal_dict["_id"])

    def set(self, field_path, value, off=None, length=None):
        if field_path == '_id' and isinstance(value, (unicode, str)):
            self.__internal_dict[field_path] = value
        elif isinstance(value, bool):
            self.__set_boolean(field_path=field_path, value=value)
        elif isinstance(value, ODate):
            self.__set_date(field_path=field_path, value=value)
        elif isinstance(value, OTime):
            self.__set_time(field_path=field_path, value=value)
        elif isinstance(value, OTimestamp):
            self.__set_timestamp(field_path=field_path, value=value)
        elif isinstance(value, OInterval):
            self.__set_interval(field_path=field_path, value=value)
        elif isinstance(value, (int, long)) and field_path != '_id':
            self.__set_long(field_path=field_path, value=value)
        elif isinstance(value, float):
            self.__set_float(field_path=field_path, value=value)
        elif isinstance(value, decimal.Decimal):
            self.__set_decimal(field_path=field_path, value=value)
        elif isinstance(value, dict):
            self.__set_dict(field_path=field_path, value=value)
        elif isinstance(value, bytearray):
            self.__set_byte_array(field_path=field_path, value=value, offset=off, length=length)
        elif isinstance(value, list):
            self.__set_array(field_path=field_path, values=value)
        elif isinstance(value, OJAIDocument):
            self.__set_document(field_path=field_path, value=value)
        elif isinstance(value, (unicode, str)):
            self.__set_str(field_path=field_path, value=value)
        elif value is None:
            self.__set_none(field_path=field_path)
        else:
            # We can set another values with help of set bool method.
            self.__set_boolean(field_path=field_path, value=value)
            # self.__internal_dict[field_path] = value
            # raise TypeError
        return self

    def parse_dict(self, dictionary):
        raise NotImplementedError

    # TODO
    def as_dictionary(self):
        return self.__internal_dict

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
                                                                ))

    def __set_float(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value,
                                                                ))

    def __set_decimal(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value.to_eng_string(),
                                                                ))

    def __set_time(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                # value=value.time_to_str(),
                                                                value=value,
                                                                ))

    def __set_date(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                # value=value.to_date_str(),
                                                                value=value,
                                                                ))

    def __set_timestamp(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                # value=value.__str__(),
                                                                value=value,
                                                                ))

    def __set_interval(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                # value=value.time_duration,
                                                                value=value,
                                                                ))

    def __set_byte_array(self, field_path, value, offset=None, length=None):
        # to_str = str(value)
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value,
                                                                ))

    def __set_dict(self, field_path, value):
        value = OJAIDict.parse_dict(value)
        if self.get(field_path) is not None:
            self.delete(field_path)
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value))

    def __set_document(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value.as_dictionary()))

    def __set_array(self, field_path, values):
        list_value = OJAIList.set_list(value=values)
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
        f = OJAIDocument.__dispatcher[t]
        f(self, field_path, value)

    def delete(self, field_path):
        split_path = [part.strip("'").strip('"') for part in self.__regex.sub(replacer,
                                                                              field_path).split("pass") if part]
        try:
            e = self.__internal_dict
            for k in split_path[:-1]:
                e = e[k]
            del e[split_path[-1]]
        except KeyError:
            pass
        return self

    def get(self, field_path):
        split_path = [part.strip("'").strip('"') for part in self.__regex.sub(replacer,
                                                                              field_path).split("pass") if part]
        value = None
        try:
            tmp_dict = self.__internal_dict
            for k in split_path[:-1]:
                tmp_dict = tmp_dict[k]
            value = tmp_dict[split_path[-1]]
        except KeyError:
            pass
        return value

    def get_str(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, (str, unicode)):
            return value
        else:
            return None

    def get_boolean(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, bool):
            return value
        else:
            return None

    def get_int(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, (int, long)) and not isinstance(value, bool):
            return value
        else:
            return None

    def get_long(self, field_path):
        return self.get_int(field_path=field_path)

    def get_float(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, float):
            return value
        else:
            return None

    def get_decimal(self, field_path):
        value = self.get(field_path=field_path)
        if value.keys()[0] == '$decimal':
            return decimal.Decimal(value.values()[0])
        else:
            return None

    def get_time(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, OTime):
            return value
        else:
            return None

    def get_date(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, ODate):
            return value
        else:
            return None

    def get_timestamp(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, OTimestamp):
            return value
        else:
            return None

    def get_binary(self, field_path):
        value = self.get(field_path=field_path)
        if value.keys()[0] == '$binary':
            return value.values()[0]
        else:
            return None

    def get_interval(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, OInterval):
            return value
        else:
            return None

    def get_value(self, field_path):
        # self.get(field_path=field_path)
        raise NotImplementedError

    def get_dictionary(self, field_path):
        value = self.get(field_path=field_path)
        if isinstance(value, dict):
            return value
        else:
            return None

    def get_list(self, field_path):
        value = self.get(field_path=field_path)
        result = []
        if isinstance(value, list):
            for element in value:
                if isinstance(element, dict):
                    result.append(element.values()[0])
                else:
                    result.append(element)
            return result
        else:
            return None

    def from_dict(self, document_dict):
        self.__internal_dict = document_dict
        return self

    def as_json_str(self, with_tags=True):
        if with_tags:
            from mapr.ojai.ojai.OJAITagsBuilder import OJAITagsBuilder
            return json.dumps(OJAITagsBuilder().set('tmp', self.__internal_dict).as_dictionary()['tmp'])
        else:
            return json.dumps(self.__internal_dict)
