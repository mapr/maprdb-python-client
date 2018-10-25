from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from past.builtins import *
standard_library.install_aliases()
from builtins import *
import json
import re

from ojai.Document import Document

from ojai.types.ODate import ODate
from ojai.types.OInterval import OInterval
from ojai.types.OTime import OTime
from ojai.types.OTimestamp import OTimestamp

from mapr.ojai.ojai import document_utils
from mapr.ojai.ojai_utils.ojai_dict import OJAIDict
from mapr.ojai.ojai_utils.ojai_list import OJAIList
from mapr.ojai.ojai.document_utils import merge_two_dicts, parse_field_path, replacer


class OJAIDocument(Document):
    __json_stream_document_reader = None
    __regex = re.compile(r"""(["']).*?\1|(?P<dot>\.)""")
    __list_regex = re.compile(r"\[(\w+)\]")

    def __init__(self, json_value=None):
        self.__internal_dict = {}
        self.json_value = json_value

    def set_id(self, _id):
        """Set _id field into the Document. _id field required for each document in MapR-DB
        :param _id: type should be binary or str"""
        if not isinstance(_id, (basestring, bytearray)):
            raise TypeError
        self.set(field_path="_id", value=_id)
        return self

    def get_id(self):
        return self.__internal_dict['_id']

    def size(self):
        return len(self.__internal_dict)

    def empty(self):
        return self.size() == 0

    def clear(self):
        self.__internal_dict = {}

    def set(self, field_path, value):
        if field_path == '_id' and isinstance(value, (basestring, bytearray)):
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
                while len(stored_value) < index:
                    stored_value.append(None)
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

    def __set_byte_array(self, field_path, value):
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

    __dispatcher = (
        (basestring, __set_str),
        (bool, __set_boolean),
        (int, __set_long),
        (float, __set_float),
        (OTime, __set_time),
        (OTimestamp, __set_timestamp),
        (ODate, __set_date),
        (OInterval, __set_interval),
        (list, __set_array),
        (dict, __set_dict),
        (bytearray, __set_byte_array),
        (None, __set_none),
    )

    def __set_dispatcher(self, field_path, value):
        for (t, m) in OJAIDocument.__dispatcher:
            if isinstance(value, t):
                return m(self, field_path, value)

    def delete(self, field_path):
        if self.__list_regex.search(field_path):
            index, stored_value = \
                self.__get_index_and_stored_value(field_path=field_path)
            del stored_value[index]
        else:
            split_path = [part.strip("'").strip('"')
                          for part in self.__regex.sub(replacer,
                                                       field_path)
                              .split("pass") if part]
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
        if isinstance(value, basestring):
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
        if isinstance(value, int) and not isinstance(value, bool):
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
                    result.append(list(element.values())[0])
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
            return json.dumps(OJAITagsBuilder().set('tmp', self.__internal_dict).as_dictionary()['tmp'],
                              default=document_utils.type_serializer)
        else:
            return json.dumps(self.__internal_dict, default=document_utils.type_serializer)
