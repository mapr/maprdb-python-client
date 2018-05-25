from mapr.ojai.storage.OJAIConnection import OJAIConnection


class ConnectionFactory:

    def __init__(self):
        pass

    @staticmethod
    def get_connection(connection_str, options=None):
        return OJAIConnection(connection_str=connection_str)
