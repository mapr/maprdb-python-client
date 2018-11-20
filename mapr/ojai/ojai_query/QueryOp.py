from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from aenum import Enum


class QueryOp(Enum):

    LESS = "$lt"

    LESS_OR_EQUAL = "$le"

    EQUAL = "$eq"

    NOT_EQUAL = "$ne"

    GREATER_OR_EQUAL = "$ge"

    GREATER = "$gt"
