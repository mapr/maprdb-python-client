from aenum import Enum


class QueryOp(Enum):

    LESS = "$lt"

    LESS_OR_EQUAL = "$le"

    EQUAL = "$eq"

    NOT_EQUAL = "$ne"

    GREATER_OR_EQUAL = "$ge"

    GREATER = "$gt"
