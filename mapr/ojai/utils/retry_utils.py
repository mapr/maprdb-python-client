from grpc import StatusCode
from grpc._channel import _Rendezvous

from mapr.ojai.exceptions.ExpiredTokenError import ExpiredTokenError

# Retry default constants
DEFAULT_WAIT_EXPONENTIAL_MULTIPLIER = 1000
DEFAULT_WAIT_EXPONENTIAL_MAX = 18000
DEFAULT_STOP_MAX_ATTEMPT = 7


# Retry option class
class RetryOptions:
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
        return exception.code() == StatusCode.UNAVAILABLE or exception.code() == StatusCode.RESOURCE_EXHAUSTED
    elif isinstance(exception, ExpiredTokenError):
        return True
    else:
        return False
