from abc import ABCMeta, abstractmethod


class Connection:
    """The Connection class defines the APIs to perform actions with storage."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_store(self, store_name, options=None):
        """Returns a handle to an OJAI DocumentStore specified by the given name or path.
        :param store_name: name or path of an OJAI data source table.
        :param options: an OJAI Document containing arbitrary, implementation specific settings"""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_document(self, json_string=None, dictionary=None):
        """Creates and returns a new, empty instance of an OJAI Document.
        :param json_string: string representation of Document.
        :param dictionary: python dict representation of Document.
        :return Document"""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_mutation(self):
        """Creates and returns a new DocumentMutation object.
        :return DocumentMutation"""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_condition(self):
        """Creates and returns a new QueryCondition object.
        :return QueryCondition"""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def new_query(self, query_json=None):
        """Creates and returns empty or decoded from query_json new Query object.
        :param query_json: QUERY json, represents as string.
        :return: Query"""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def close(self):
        """Close connection with server."""
        raise NotImplementedError("Should have implemented this")
