from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from past.builtins import *
from ojai.store.DocumentMutation import DocumentMutation

from mapr.ojai.document.MutationOp import MutationOp
from mapr.ojai.document.MutationUtil import MutationUtil
from mapr.ojai.exceptions.DocumentMutationError import DocumentMutationError
from mapr.ojai.exceptions.IllegalArgumentError import IllegalArgumentError
from mapr.ojai.ojai.OJAIDocument import OJAIDocument


def validate_field_path(f):
    def wrapper(*args, **kwargs):
        if (kwargs.get('field_path', None) or args[1]) == '_id':
            raise IllegalArgumentError('The _id field cannot be set or updated')
        return f(*args, **kwargs)

    return wrapper


class OJAIDocumentMutation(DocumentMutation):

    def __init__(self):
        self.__mutation_dict = {}
        self.__doc = OJAIDocument()

    @staticmethod
    def mutation_common(op):
        if op == MutationOp.NONE:
            raise DocumentMutationError('Mutation can\'t have NONE type')
        return op.value

    def empty(self):
        self.__mutation_dict = {}

    @validate_field_path
    def set(self, field_path, value):
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=value,
                                         operation_type=MutationOp.SET,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    @validate_field_path
    def set_or_replace(self, field_path, value):
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=value,
                                         operation_type=MutationOp.SET_OR_REPLACE,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    @validate_field_path
    def append(self, field_path, value, offset=None, length=None):
        if not isinstance(value, (list, basestring, bytearray)):
            raise TypeError('Value type is not supported. Must be list, str, bytearray')
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=value,
                                         operation_type=MutationOp.APPEND,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    @validate_field_path
    def merge(self, field_path, value):
        if not isinstance(value, (OJAIDocument, dict)):
            raise TypeError('Value must be only Document or dict')
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=value if isinstance(value, dict) else value.as_dictionary(),
                                         operation_type=MutationOp.MERGE,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    @validate_field_path
    def increment(self, field_path, inc=None):
        if inc is None:
            inc = 1
        if not isinstance(inc, (int, float))\
                or isinstance(inc, bool):
            raise TypeError('Field path value can only be int, long or float.')
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=inc,
                                         operation_type=MutationOp.INCREMENT,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    @validate_field_path
    def decrement(self, field_path, dec=None):
        if dec is None:
            dec = 1
        if not isinstance(dec, (int, float))\
                or isinstance(dec, bool):
            raise TypeError('Field path value can only be int, long or float.')
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=dec,
                                         operation_type=MutationOp.DECREMENT,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    @validate_field_path
    def delete(self, field_path):
        self.__mutation_dict = \
            MutationUtil.delete(path=field_path,
                                operation_type=MutationOp.DELETE,
                                mutation_dict=self.__mutation_dict,
                                doc=self.__doc)
        return self

    def as_dict(self):
        return self.__mutation_dict
