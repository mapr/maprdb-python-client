from abc import ABCMeta, abstractmethod


class DriverManager:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_driver(self, url):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def get_connection(self, url, options=None):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def register_driver(self, driver):
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def check_url(self, url):
        raise NotImplementedError("Should have implemented this")