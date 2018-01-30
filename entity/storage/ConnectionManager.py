from abc import ABCMeta, abstractmethod


class ConnectionManager:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_connection(self, url, options=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def check_url(self, url):
        raise NotImplementedError("Should have implemented this")