from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
class PathNotFoundError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message
