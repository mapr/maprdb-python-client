from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from grpc import StatusCode
from grpc._channel import _Rendezvous

from mapr.ojai.exceptions.ExpiredTokenError import ExpiredTokenError

# Retry default constants
DEFAULT_WAIT_EXPONENTIAL_MULTIPLIER = 1000
DEFAULT_WAIT_EXPONENTIAL_MAX = 18000
DEFAULT_STOP_MAX_ATTEMPT = 7


# Retry option class
class RetryOptions(object):
    def __init__(self,
                 wait_exponential_multiplier,
                 wait_exponential_max,
                 stop_max_attempt_number):
        self.wait_exponential_multiplier = wait_exponential_multiplier
        self.wait_exponential_max = wait_exponential_max
        self.stop_max_attempt_number = stop_max_attempt_number


# Retry checker function
def retry_if_connection_not_established(exception):
    if isinstance(exception, _Rendezvous):
        if exception.code() == StatusCode.UNAUTHENTICATED \
                and exception.details() == 'STATUS_TOKEN_EXPIRED':
            return True
        else:
            return exception.code() == StatusCode.UNAVAILABLE \
                   or exception.code() == StatusCode.RESOURCE_EXHAUSTED
    elif isinstance(exception, ExpiredTokenError):
        return True
    else:
        return False
