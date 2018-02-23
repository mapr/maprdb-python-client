from mapr.ojai.storage.ConnectionImpl import ConnectionImpl


class ConnectionManagerImpl:

    def __init__(self):
        pass

    @staticmethod
    def get_connection(url, options=None):
        return ConnectionImpl(connection_url=url)
