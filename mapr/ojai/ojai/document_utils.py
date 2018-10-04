from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from copy import deepcopy

import re

from ojai.types.ODate import ODate
from ojai.types.OInterval import OInterval
from ojai.types.OTime import OTime
from ojai.types.OTimestamp import OTimestamp

__regex = re.compile(r"""(["']).*?\1|(?P<dot>\.)""")


def parse_list(values_list):
    from mapr.ojai.ojai.OJAITagsBuilder import OJAITagsBuilder
    temp_doc = OJAITagsBuilder()
    parsed_list = []
    for element in values_list:
        temp_doc.set('parse_list', element)
        parsed_list.append(temp_doc.as_dictionary()['parse_list'])

    return parsed_list


def parse_field_path(field_path, value, oja_type=None):
    split_path = [part.strip("'").strip('"') for part in __regex.sub(replacer,
                                                                     field_path).split("pass") if part]
    tmp_dict = {}

    for i in reversed(split_path):
        if tmp_dict == {}:
            if oja_type is None:
                tmp_dict = {i: value}
            else:
                tmp_dict = {i: {oja_type: value}}
        else:
            tmp_dict = {i: tmp_dict}

    return tmp_dict


def merge_list_value(merged_dict, k, v):
    working_dict = merged_dict
    swap = False
    for dict_element in working_dict[k]:
        if isinstance(dict_element, (list, dict)):
            for elem_k in dict_element:
                if isinstance(v, list):
                    for item in v:
                        if elem_k in item:
                            index = working_dict[k].index(dict_element)
                            working_dict[k].remove(dict_element)
                            working_dict[k].insert(index, item)
                            swap = True
                else:
                    if elem_k in v:
                        index = working_dict[k].index(dict_element)
                        working_dict[k].remove(dict_element)
                        working_dict[k].insert(index, v)
                        swap = True
    if not swap:
        working_dict[k] = v
        return working_dict
    return working_dict


def merge_two_dicts(dict1, dict2):
    if not isinstance(dict2, dict):
        return dict2
    merged_dict = deepcopy(dict1)
    for k, v in list(dict2.items()):
        if k in merged_dict and isinstance(merged_dict[k], dict):
            merged_dict[k] = merge_two_dicts(merged_dict[k], v)
        elif k in merged_dict and isinstance(merged_dict[k], list):
            merged_dict = merge_list_value(merged_dict=merged_dict, k=k, v=v)
        else:
            if k in ('$numberLong', '$numberFloat', '$numberShort', '$binary',
                     '$interval', '$date', '$dateDay', '$time') and len(merged_dict) == 1:
                merged_dict = dict2
            else:
                merged_dict[k] = deepcopy(v)
    return merged_dict


def replacer(match):
    if match.group('dot') is not None:
        return "pass"
    else:
        return match.group(0)


def type_serializer(obj):
    try:
        return obj.toJSON()
    except:
        if isinstance(obj, (OTime, ODate, OTimestamp, OInterval)):
            return obj.__str__()
        elif isinstance(obj, (bytearray, bytes)):
            return obj.decode('utf8')
        else:
            return obj.__dict__
