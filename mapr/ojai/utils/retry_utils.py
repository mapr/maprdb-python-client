from grpc._channel import _Rendezvous


def retry_if_connection_not_established(exception):
    return isinstance(exception, _Rendezvous)
# TODO config and exp time
