from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from mapr.ojai.storage.OJAIConnection import OJAIConnection


class ConnectionFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def get_connection(connection_str, options=None):
        """
        Connection factory for OJAIConnection.
        Example:
        connection_str = 'localhost:5678?auth=basic;user=mapr;password=mapr;' \
          'ssl=true;' \
          'sslCA=/opt/mapr/conf/ssl_truststore.pem;' \
          'sslTargetNameOverride=node1.mapr.com'
        options = {
            'ojai.mapr.rpc.wait-multiplier': 5,
            'ojai.mapr.rpc.wait-max-attempt': 50,
            'ojai.mapr.rpc.max-retries': 3
        }
        connection = ConnectionFactory.get_connection(connection_str=connection_str,
                                          options=options)
        :param connection_str: connection string
        :param options: options as dict
        :return: OJAIConnection instance
        """
        return OJAIConnection(connection_str=connection_str, options=options)
