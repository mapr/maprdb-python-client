import json
import re
from copy import deepcopy

import decimal
from ojai.document.Document import Document

from mapr.ojai.o_types.ODate import ODate
from mapr.ojai.o_types.OInterval import OInterval
from mapr.ojai.o_types.OTime import OTime
from mapr.ojai.o_types.OTimestamp import OTimestamp
from mapr.ojai.ojai.OJAIList import OJAIList


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
        # check that _id value is str, int or long, otherwise raise TypeError
        # if type(_id) not in [int, str, long]:
        if not isinstance(_id, (unicode, str, int, long)):
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
        if field_path == '_id' and isinstance(value, (unicode, str, int, long)):
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
        elif isinstance(value, str):
            self.__set_str(field_path=field_path, value=value)
        elif value is None:
            self.__set_none(field_path=field_path)
        else:
            # We can set another values with help of set bool method.
            self.__set_boolean(field_path=field_path, value=value)
            # self.__internal_dict[field_path] = value
            # raise TypeError
        return self

    def __merge_two_dicts(self, dict1, dict2):
        if not isinstance(dict2, dict):
            return dict2
        merged_dict = deepcopy(dict1)
        for k, v in dict2.iteritems():
            if k in merged_dict and isinstance(merged_dict[k], dict):
                merged_dict[k] = self.__merge_two_dicts(merged_dict[k], v)
            else:
                merged_dict[k] = deepcopy(v)
        return merged_dict

    def __replacer(self, match):
        if match.group('dot') is not None:
            return "pass"
        else:
            return match.group(0)

    def __parse_list(self, values_list):
        temp_doc = OJAIDocument()
        parsed_list = []
        for element in values_list:
            temp_doc.set('parse_list', element)
            parsed_list.append(temp_doc.as_dictionary()['parse_list'])

        return parsed_list

    def __parse_field_path(self, field_path, value, oja_type=None):
        split_path = [part.strip("'").strip('"') for part in self.__regex.sub(self.__replacer,
                                                                              field_path).split("pass") if part]
        tmp_dict = {}

        for i in reversed(split_path):
            if tmp_dict == {}:
                # if isinstance(value, list):
                #     parsed_list = self.__parse_list(values_list=value)
                #     tmp_dict = {i: parsed_list}
                # el
                if oja_type is None:
                    tmp_dict = {i: value}
                else:
                    tmp_dict = {i: {oja_type: value}}
            else:
                tmp_dict = {i: tmp_dict}

        return tmp_dict

    def as_dictionary(self):
        return self.__internal_dict

    def __set_str(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value))

    def __set_boolean(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value))

    # We can't check byte, because we can only create a custom value type, which represent as str.
    # def __set_byte(self, field_path, value):
    #     pass

    def __set_long(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value,
                                                                              oja_type='$numberLong'))
        # self.__internal_dict[field_path] = {'$numberLong': value}

    def __set_float(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value,
                                                                              oja_type='$numberFloat'))

    def __set_decimal(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value.to_eng_string(),
                                                                              oja_type='$decimal'))

    def __set_time(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value.time_to_str(),
                                                                              oja_type='$time'))

    def __set_date(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value.to_date_str(),
                                                                              oja_type='$dateDay'))
        # self.__internal_dict[field_path] = {'$dateDay': value.to_date_str()}

    def __set_timestamp(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value.__str__(),
                                                                              oja_type='$date'))
        # self.__internal_dict[field_path] = {'$date': value.__str__()}

    def __set_interval(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value.time_duration,
                                                                              oja_type='$interval'))

    def __set_byte_array(self, field_path, value, offset=None, length=None):
        # TODO clarify how to keep array of byte
        to_str = str(value)
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=to_str,
                                                                              oja_type='$binary'))

    def __set_dict(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value))

    def __set_document(self, field_path, value):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=value.as_dictionary()))

    # TODO why we need a JsonValue?
    # def __set_value_obj(self, field_path, value):
    #     pass

    def __set_array(self, field_path, values):
        list_value = OJAIList.set_list(value=values)
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
                                                                              value=list_value))

    def __set_none(self, field_path):
        self.__internal_dict = self.__merge_two_dicts(self.__internal_dict,
                                                      self.__parse_field_path(field_path=field_path,
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
        split_path = [part.strip("'").strip('"') for part in self.__regex.sub(self.__replacer,
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
        split_path = [part.strip("'").strip('"') for part in self.__regex.sub(self.__replacer,
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

    def get_string(self, field_path):
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
        if value.keys()[0] == '$numberLong':
            return value.values()[0]
        else:
            return None

    def get_long(self, field_path):
        value = self.get(field_path=field_path)
        if value.keys()[0] == '$numberLong':
            return value.values()[0]
        else:
            return None

    def get_float(self, field_path):
        value = self.get(field_path=field_path)
        if value.keys()[0] == '$numberFloat':
            return value.values()[0]
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
        if value.keys()[0] == '$time':
            time = OTime.parse(value.values()[0])
            return time
        else:
            return None

    def get_date(self, field_path):
        value = self.get(field_path=field_path)
        if value.keys()[0] == '$dateDay':
            date = ODate.parse(value.values()[0])
            return date
        else:
            return None

    def get_timestamp(self, field_path):
        value = self.get(field_path=field_path)
        if value.keys()[0] == '$date':
            timestamp = OTimestamp.parse(value.values()[0])
            return timestamp
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
        if value.keys()[0] == '$interval':
            interval = OInterval(milli_seconds=value.values()[0])
            return interval
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

    # TODO implement ability to parse dict without OJAI tags
    def as_json_str(self, with_tags=None):
        return json.dumps(self.__internal_dict, indent=4)
