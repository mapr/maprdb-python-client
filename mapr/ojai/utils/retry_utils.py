from grpc import StatusCode
from grpc._channel import _Rendezvous


def retry_if_connection_not_established(exception):
    if isinstance(exception, _Rendezvous):
        return exception.code() == StatusCode.UNAVAILABLE or exception.code() == StatusCode.RESOURCE_EXHAUSTED
    else:
        return False
# TODO config and exp time
