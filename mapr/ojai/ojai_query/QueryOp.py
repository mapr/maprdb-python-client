from aenum import Enum

class OJAIQueryCondition(Enum):
    # A non-existing value of unknown type and quantity.
    LESS = 1

    # A boolean value.
    LESS_OR_EQUAL = 2

    # Character sequence.
    EQUAL = 3

    # Bytes represent as string
    NOT_EQUAL = 4

    # Integer
    GREATER_OR_EQUAL = 5
    GREATER = 5