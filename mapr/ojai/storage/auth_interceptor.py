from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import next
from builtins import object
import base64
import collections
import grpc

from mapr.ojai.exceptions.ExpiredTokenError import ExpiredTokenError


class _ClientAuthInterceptor(
        grpc.UnaryUnaryClientInterceptor, grpc.UnaryStreamClientInterceptor):

    def __init__(self, interceptor_function, user_metadata):
        self._fn = interceptor_function
        self._user_metadata = user_metadata

    def intercept_unary_unary(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, iter((request,)))
        response = continuation(new_details, next(new_request_iterator))
        self._user_metadata.set_jwt_token(response)
        return postprocess(response) if postprocess else response

    def intercept_unary_stream(self, continuation, client_call_details,
                               request):

        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, iter((request,)))
        response_it = continuation(new_details, next(new_request_iterator))
        self._user_metadata.set_jwt_token(response_it, True)
        return postprocess(response_it) if postprocess else response_it


class __UserMetadata(object):

    def __init__(self, encoded_user_metadata):
        self._token = None
        self._encoded_user_creds = encoded_user_metadata

    def metadata_builder(self):
        if not self._token:
            value = 'basic {0}'.format(self._encoded_user_creds)
        else:
            value = 'bearer {0}'.format(self._token)
            self._token = None
        return 'authorization', value

    def set_jwt_token(self, call, stream=False):
        if not self._token:
            try:
                self._token = \
                        dict(call.initial_metadata())['bearer-token']
            except:
                pass
        elif stream:
            if call.done() and call.code() == grpc.StatusCode.UNAUTHENTICATED \
                    and call.details() == 'STATUS_TOKEN_EXPIRED':
                    self._token = None
                    raise ExpiredTokenError()
        elif call.code() == grpc.StatusCode.UNAUTHENTICATED \
                and call.details() == 'STATUS_TOKEN_EXPIRED':
            self._token = None
            raise ExpiredTokenError()


class _ClientCallDetails(
        collections.namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')),
        grpc.ClientCallDetails):
    pass


def client_auth_interceptor(encoded_user_metadata):
    user_metadata = __UserMetadata(encoded_user_metadata)

    def intercept_call(client_call_details, request_iterator):
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append((user_metadata.metadata_builder()))

        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials)
        return client_call_details, request_iterator, None

    return _ClientAuthInterceptor(intercept_call, user_metadata)
