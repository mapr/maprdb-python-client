from mapr.ojai.storage.OJAIConnection import OJAIConnection


class ConnectionFactory:

    def __init__(self):
        pass

    @staticmethod
    def get_connection(url, options=None):
        return OJAIConnection(connection_url=url)
