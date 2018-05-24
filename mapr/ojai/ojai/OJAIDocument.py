import json
import re
from copy import deepcopy

import decimal

from datetime import datetime
from ojai.Document import Document

from ojai.types.ODate import ODate
from ojai.types.OInterval import OInterval
from ojai.types.OTime import OTime
from ojai.types.OTimestamp import OTimestamp
from mapr.ojai.ojai.OJAIDict import OJAIDict
from mapr.ojai.ojai.OJAIList import OJAIList
from mapr.ojai.ojai.document_utils import merge_two_dicts, parse_field_path, replacer


class OJAIDocument(Document):

    # Not needed?
    def get_byte(self, field_path):
        pass

    __json_stream_document_reader = None
    __regex = re.compile(r"""(["']).*?\1|(?P<dot>\.)""")
    __list_regex = re.compile(r"\[(\w+)\]")

    def __init__(self, json_value=None):
        self.__internal_dict = {}
        self.json_value = json_value

    def set_id(self, _id):
        """Set _id field into the Document. _id field required for each document in MapR-DB
        :param _id: type should be binary or str"""
        if not isinstance(_id, (unicode, str, bytearray)):
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
        if field_path == '_id' and isinstance(value, (unicode, str, bytearray)):
            self.__internal_dict[field_path] = value
        elif self.__list_regex.search(field_path):
            self.__set_list_element(field_path=field_path, value=value)
        elif isinstance(value, OJAIDocument):
            self.__set_document(field_path=field_path, value=value)
        elif value is None:
            self.__set_none(field_path=field_path)
        else:
            self.__set_dispatcher(field_path=field_path, value=value)

        return self

    def __get_index_and_stored_value(self, field_path):
        index = int(self.__list_regex.search(field_path).group(1))
        stored_value = self.get(re.sub(self.__list_regex, '', field_path))
        return index, stored_value

    def __set_list_element(self, field_path, value):
        index, stored_value = self.__get_index_and_stored_value(field_path=field_path)

        if isinstance(stored_value, list):
            if len(stored_value) < index:
                stored_value.append(value)
            else:
                stored_value[index] = value

    def parse_dict(self, dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError("parse_dict allows only dict as input param.")
        self.__internal_dict = dictionary
        return self

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
                                                                value=value,
                                                                ))

    def __set_time(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value,
                                                                ))

    def __set_date(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value,
                                                                ))

    def __set_timestamp(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value,
                                                                ))

    def __set_interval(self, field_path, value):
        self.__internal_dict = merge_two_dicts(self.__internal_dict,
                                               parse_field_path(field_path=field_path,
                                                                value=value,
                                                                ))

    def __set_byte_array(self, field_path, value, offset=None, length=None):
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

    def __set_array(self, field_path, value):
        list_value = OJAIList.set_list(value=value)
        if self.get(field_path) is not None:
            self.delete(field_path)
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
        value = None
        index = None
        if self.__list_regex.search(field_path):
            index = int(self.__list_regex.search(field_path).group(1))
            field_path = re.sub(self.__list_regex, '', field_path)

        split_path = [part.strip("'").strip('"') for part in self.__regex.sub(replacer,
                                                                              field_path).split("pass") if part]
        try:
            tmp_dict = self.__internal_dict
            for k in split_path[:-1]:
                tmp_dict = tmp_dict[k]
            value = tmp_dict[split_path[-1]]
        except KeyError:
            pass
        if index is not None and value is not None and isinstance(value, list):
            try:
                value = value[index]
            except IndexError:
                value = None
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
        if isinstance(value, decimal.Decimal):
            return value
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
        if isinstance(value, bytearray):
            return value
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

    @staticmethod
    def __type_serializer(obj):
        try:
            return obj.toJSON()
        except:
            if isinstance(obj, (OTime, ODate, OTimestamp, OInterval)):
                return obj.__str__()
            else:
                return obj.__dict__

    def as_json_str(self, with_tags=True):
        if with_tags:
            from mapr.ojai.ojai.OJAITagsBuilder import OJAITagsBuilder
            return json.dumps(OJAITagsBuilder().set('tmp', self.__internal_dict).as_dictionary()['tmp'])
        else:
            return json.dumps(self.__internal_dict, default=OJAIDocument.__type_serializer)
