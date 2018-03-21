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

    def __merge_two_dicts(self, dict1, dict2):
        """Function merge two dictionaries into one without data loss"""
        if not isinstance(dict2, dict):
            return dict2
        merged_dict = deepcopy(dict1)
        for k, v in dict2.iteritems():
            if k in merged_dict and isinstance(merged_dict[k], dict):
                merged_dict[k] = self.__merge_two_dicts(merged_dict[k], v)
            elif k in merged_dict and isinstance(merged_dict[k], list):
                swap = False
                for dict_element in merged_dict[k]:
                    for elem_k in dict_element:
                        if isinstance(v, list):
                            for item in v:
                                if elem_k in item:
                                    index = merged_dict[k].index(dict_element)
                                    merged_dict[k].remove(dict_element)
                                    merged_dict[k].insert(index, item)
                                    swap = True
                        else:
                            if elem_k in v:
                                index = merged_dict[k].index(dict_element)
                                merged_dict[k].remove(dict_element)
                                merged_dict[k].insert(index, v)
                                swap = True
                if not swap:
                    merged_dict[k].append(v)
            else:
                merged_dict[k] = deepcopy(v)
        return merged_dict

    def __convert_values(self, values):
        """Converting all values in the list to str
        :param values: list of params
        :return list where each element is str"""
        return map(str, values)

    def set_option(self, option_name, value=None):
        pass

    # TODO $options
    def set_options(self, options):
        pass

    # TODO need
    def set_timeout(self, timeout_in_millis):
        pass

    def select(self, field_paths):
        if not isinstance(field_paths, list):
            raise TypeError()
        self.__query_dict = self.__merge_two_dicts(self.__query_dict,
                                                   {Operations.SELECT: self.__convert_values(field_paths)})

        return self

    def where(self, condition):
        if not isinstance(condition, OJAIQueryCondition) and not isinstance(condition, dict):
            raise TypeError("Condition type must be OJAIQueryCondition or dict.")
        self.__query_dict = self.__merge_two_dicts(self.__query_dict,
                                                   {Operations.WHERE: condition.as_dictionary()})
        return self

    def order_by(self, field_paths, order='asc'):
        if not isinstance(field_paths, (str, unicode, list)):
            raise TypeError()
        self.__query_dict = self.__merge_two_dicts(self.__query_dict,
                                                   {Operations.ORDER_BY:
                                                    {field_paths: order} if isinstance(field_paths, (unicode, str))
                                                    # else [{field: order} for field in field_paths]})
                                                    else map(lambda field: {field: order}, field_paths)})
        return self

    def offset(self, offset):
        if not isinstance(offset, (int, long)) or offset < 0:
            raise TypeError
        self.__query_dict = self.__merge_two_dicts(self.__query_dict, {Operations.OFFSET: offset})

        return self

    def limit(self, limit):
        if not isinstance(limit, (int, long)) or limit < 0:
            raise TypeError
        self.__query_dict = self.__merge_two_dicts(self.__query_dict, {Operations.LIMIT: limit})

        return self

    def build(self):
        self.__is_build = True
        return self

    def to_json_str(self):
        if self.__is_build:
            return json.dumps(self.__query_dict, indent=4)
        else:
            raise QueryNotBuildError('Build query with help of build() method.')

    def query_dict(self):
        if self.__is_build:
            return self.__query_dict
        else:
            raise QueryNotBuildError('Build query with help of build() method.')


class Operations(enum):
    SELECT = "$select"

    WHERE = "$where"

    ORDER_BY = "$orderby"

    OFFSET = "$offset"

    LIMIT = "$limit"
