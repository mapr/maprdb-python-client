from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from past.builtins import *
from builtins import *
from builtins import map
import json
from copy import deepcopy

from aenum import enum
from ojai.store.Query import Query

from mapr.ojai.exceptions.QueryNotBuildError import QueryNotBuildError
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition


class OJAIQuery(Query):

    def __init__(self):
        self.__query_dict = {}
        self.__is_build = False

    def __merge_list_value(self, merged_dict, k, v):
        working_dict = merged_dict
        swap = False
        for dict_element in working_dict[k]:
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
            working_dict[k].append(v)
        return working_dict

    def __merge_two_dicts(self, dict1, dict2):
        """Function merge two dictionaries into one without data loss"""
        if not isinstance(dict2, dict):
            return dict2
        merged_dict = deepcopy(dict1)
        for k, v in list(dict2.items()):
            if k in merged_dict and isinstance(merged_dict[k], dict):
                merged_dict[k] = self.__merge_two_dicts(merged_dict[k], v)
            elif k in merged_dict and isinstance(merged_dict[k], list):
                merged_dict = self.__merge_list_value(merged_dict=merged_dict, k=k, v=v)
            else:
                merged_dict[k] = deepcopy(v)
        return merged_dict

    def __convert_values(self, values):
        """Converting all values in the list to str
        :param values: list of params
        :return list where each element is str"""
        return list(map(str, values))

    def select(self, *args):
        field_paths = []
        for arg in args:
            if isinstance(arg, list):
                field_paths = field_paths + arg
            elif isinstance(arg, basestring):
                field_paths.append(arg)
            else:
                raise TypeError

        self.__query_dict = self.__merge_two_dicts(self.__query_dict,
                                                   {Operations.SELECT: self.__convert_values(field_paths)})

        return self

    def where(self, condition):
        if not isinstance(condition, (OJAIQueryCondition, dict, basestring)):
            raise TypeError("Condition type must be OJAIQueryCondition or dict.")

        if isinstance(condition, OJAIQueryCondition):
            if condition.is_empty():
                raise AttributeError("Condition can't be empty.")
            self.__query_dict = self.__merge_two_dicts(self.__query_dict,
                                                       {Operations.WHERE: condition.as_dictionary()})
        elif isinstance(condition, basestring):
            if not condition:
                raise AttributeError("Condition can't be empty.")
            self.__query_dict = self.__merge_two_dicts(self.__query_dict,
                                                       {Operations.WHERE: json.loads(condition)})
        else:
            if not condition:
                raise AttributeError("Condition can't be empty.")
            self.__query_dict = self.__merge_two_dicts(self.__query_dict,
                                                       {Operations.WHERE: condition})
        return self

    def order_by(self, field_paths, order='asc'):
        if not isinstance(field_paths, (basestring, list)) or not field_paths:
            raise TypeError('The field paths type can be either str or list and cannot be empty.')
        self.__query_dict = self.__merge_two_dicts(self.__query_dict,
                                                   {Operations.ORDER_BY:
                                                    {field_paths: order} if isinstance(field_paths, basestring)
                                                    else [{field: order} for field in field_paths]})
        return self

    def offset(self, offset):
        if not isinstance(offset, int) or offset < 0 or isinstance(offset, bool):
            raise TypeError
        self.__query_dict = self.__merge_two_dicts(self.__query_dict, {Operations.OFFSET: offset})

        return self

    def limit(self, limit):
        if not isinstance(limit, int) or limit < 0 or isinstance(limit, bool):
            raise TypeError
        self.__query_dict = self.__merge_two_dicts(self.__query_dict, {Operations.LIMIT: limit})

        return self

    def build(self):
        self.__is_build = True
        return self

    def to_json_str(self):
        if self.__is_build:
            return json.dumps(self.__query_dict)
        else:
            raise QueryNotBuildError('Build query with help of build() method.')

    def query_dict(self):
        if self.__is_build:
            return self.__query_dict
        else:
            raise QueryNotBuildError('Build query with help of build() method.')

    def from_dict(self, query_dict):
        self.__query_dict = query_dict
        return self

    def from_json(self, json_query):
        self.from_dict(query_dict=json.loads(json_query))
        return self


class Operations(enum):
    SELECT = "$select"

    WHERE = "$where"

    ORDER_BY = "$orderby"

    OFFSET = "$offset"

    LIMIT = "$limit"
