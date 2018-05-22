from ojai.store.DocumentMutation import DocumentMutation

from mapr.ojai.document.MutationOp import MutationOp
from mapr.ojai.document.MutationUtil import MutationUtil
from mapr.ojai.exceptions.DocumentMutationError import DocumentMutationError
from mapr.ojai.exceptions.FieldPathAlreadyInDocumentError import \
    FieldPathAlreadyInDocumentError
from mapr.ojai.ojai.OJAIDocument import OJAIDocument


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

    def set(self, field_path, value):
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=value,
                                         operation_type=MutationOp.SET,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    def set_or_replace(self, field_path, value):
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=value,
                                         operation_type=
                                         MutationOp.SET_OR_REPLACE,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    def append(self, field_path, value, offset=None, length=None):
        if not isinstance(value, (list, str, bytearray)):
            raise TypeError('Value type is not supported. Must be list, str, bytearray')
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=value,
                                         operation_type=MutationOp.APPEND,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    def merge(self, field_path, value):
        if not isinstance(value, (OJAIDocument, dict)):
            raise TypeError('Value must be only Document or dict')
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=value,
                                         operation_type=MutationOp.MERGE,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    def increment(self, field_path, inc=None):
        if inc is None:
            inc = 1
        # TODO add decimal
        if not isinstance(inc, (int, long, float)):
            raise TypeError('Value must be only Document or dict')
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=inc,
                                         operation_type=MutationOp.INCREMENT,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    def decrement(self, field_path, dec=None):
        if dec is None:
            dec = -1
        if not isinstance(dec, (int, long, float)):
            raise TypeError('Value must be only Document or dict')
        self.__mutation_dict = \
            MutationUtil.evaluate_common(path=field_path,
                                         value=dec,
                                         operation_type=MutationOp.DECREMENT,
                                         mutation_dict=self.__mutation_dict,
                                         doc=self.__doc)
        return self

    def delete(self, field_path):
        self.__mutation_dict = \
            MutationUtil.delete(path=field_path,
                                operation_type=MutationOp.DELETE,
                                mutation_dict=self.__mutation_dict,
                                doc=self.__doc)
        return self

    def as_dict(self):
        return self.__mutation_dict
