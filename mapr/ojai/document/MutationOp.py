from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
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
