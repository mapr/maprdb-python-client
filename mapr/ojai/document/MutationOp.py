from aenum import Enum


class MutationOp(Enum):
    NONE = 0
    SET_OR_REPLACE = '$put'
    SET = '$set'
    DELETE = '$delete'
    APPEND = '$append'
    INCREMENT = '$increment'
    DECREMENT = '$decrement'
    MERGE = '$merge'
