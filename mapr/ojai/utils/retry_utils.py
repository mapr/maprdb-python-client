from grpc import StatusCode
from grpc._channel import _Rendezvous

from mapr.ojai.exceptions.ExpiredTokenError import ExpiredTokenError


def retry_if_connection_not_established(exception):
    if isinstance(exception, _Rendezvous):
        return exception.code() == StatusCode.UNAVAILABLE or exception.code() == StatusCode.RESOURCE_EXHAUSTED
    elif isinstance(exception, ExpiredTokenError):
        return True
    else:
        return False
# TODO config and exp time
