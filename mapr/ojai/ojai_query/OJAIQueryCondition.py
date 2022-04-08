from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from past.builtins import *
from copy import deepcopy
from collections import deque

from ojai.store.QueryCondition import QueryCondition

from mapr.ojai.exceptions.ConditionNotClosedError import ConditionNotClosedError
from mapr.ojai.exceptions.InvalidArgumentError import InvalidArgumentError
from mapr.ojai.ojai_query.QueryOp import QueryOp


class OJAIQueryCondition(QueryCondition):

    def __init__(self):
        self.__tokens = deque()
        self.__query_dict = {}
        self.__is_built = False

    def __merge_two_dicts(self, dict1, dict2):
        """Function merge two dictionaries into one without data loss"""
        if not isinstance(dict2, dict):
            return dict2
        merged_dict = deepcopy(dict1)
        for k, v in list(dict2.items()):
            if k in merged_dict and isinstance(merged_dict[k], dict):
                merged_dict[k] = self.__merge_two_dicts(merged_dict[k], v)
            else:
                merged_dict[k] = deepcopy(v)
        return merged_dict

    def is_empty(self):
        return not bool(self.__query_dict)

    def is_built(self):
        return self.__is_built

    def and_(self):
        self.__tokens.append('$and')
        return self

    def or_(self):
        self.__tokens.append('$or')
        return self

    def element_and(self, field_path):
        if not isinstance(field_path, basestring) or not field_path:
            raise InvalidArgumentError(m='field path must be str or unicode.')
        self.__tokens.append('$elementAnd')
        self.__tokens.append(field_path)
        return self

    def close(self):
        self.__tokens.append(';')
        return self

    def condition_(self, condition_to_add):
        if isinstance(condition_to_add, OJAIQueryCondition):
            if condition_to_add.is_built():
                self.__tokens.append(condition_to_add.as_dictionary())
            else:
                self.__tokens.append(condition_to_add.build().as_dictionary())
        elif isinstance(condition_to_add, dict):
            self.__tokens.append(condition_to_add)
        else:
            raise TypeError
        return self

    def exists_(self, field_path):
        self.__tokens.append({'$exists': field_path})
        return self

    def not_exists_(self, field_path):
        self.__tokens.append({'$notexists': field_path})
        return self

    def in_(self, field_path, list_of_value):
        self.__tokens.append({'$in': {field_path: list_of_value}})
        return self

    def not_in_(self, field_path, list_of_value):
        self.__tokens.append({'$notin': {field_path: list_of_value}})
        return self

    def type_of_(self, field_path, value_type):
        self.__tokens.append({'$typeof': {field_path: value_type}})
        return self

    def not_type_of_(self, field_path, value_type):
        self.__tokens.append({'$nottypeof': {field_path: value_type}})
        return self

    def matches_(self, field_path, regex):
        self.__tokens.append({'$matches': {field_path: regex}})
        return self

    def not_matches_(self, field_path, regex):
        self.__tokens.append({'$notmatches': {field_path: regex}})
        return self

    def like_(self, field_path, like_expression, escape_char=None):
        self.__tokens.append({'$like': {field_path: [like_expression, escape_char] if escape_char else like_expression}})
        return self

    def not_like_(self, field_path, like_expression, escape_char=None):
        self.__tokens.append({'$notlike': {field_path: [like_expression, escape_char] if escape_char else like_expression}})
        return self

    def is_(self, field_path, op, value):
        self.__tokens.append({op.value: {field_path: value}})

        return self

    def equals_(self, field_path, value):
        self.__tokens.append({QueryOp.EQUAL.value: {field_path: value}})
        return self

    def not_equals_(self, field_path, value):
        self.__tokens.append({QueryOp.NOT_EQUAL.value: {field_path: value}})
        return self

    def size_of_(self, field_path, op, size):
        pass

    def __parse(self, tokens):
        while tokens:
            token = tokens.popleft()
            if not tokens:
                if token != ';':
                    raise ConditionNotClosedError("All statement in condition must be closed.")
                else:
                    continue

            if token in ['$and', '$or', '$elementAnd']:
                self.__query_dict = \
                    self.__merge_two_dicts(self.__query_dict,
                                           self.__build_block(tokens, token))
            elif isinstance(token, dict):
                self.__query_dict = self.__merge_two_dicts(self.__query_dict, token)
            elif token == ';' and tokens:
                raise ConditionNotClosedError("All statement in condition must be closed.")
        return self.__query_dict

    def __build_block(self, tokens, op):
        statement_list = []
        element_and_fp = None
        if op == '$elementAnd':
            element_and_fp = tokens.popleft()
        while tokens:
            token = tokens.popleft()
            if token in ['$and', '$or', '$elementAnd']:
                statement_list.append(self.__build_block(tokens, token))
            elif token == ';':
                if not element_and_fp:
                    return {op: statement_list}
                else:
                    return {op: {element_and_fp: statement_list}}
            else:
                statement_list.append(token)

        raise ConditionNotClosedError("All statement in condition must be closed.")

    def build(self):
        self.__query_dict = self.__parse(self.__tokens)
        self.__is_built = True
        return self

    def as_dictionary(self):
        return self.__query_dict
