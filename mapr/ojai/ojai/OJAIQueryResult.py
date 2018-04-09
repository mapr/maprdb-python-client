from ojai.store.QueryResult import QueryResult


class OJAIQueryResult(QueryResult):

    def __init__(self, query_plan, document_stream):
        self.__query_plan = query_plan
        self.__doc_stream = document_stream

    def iterator(self):
        return self.__doc_stream

    def get_query_plan(self):
        return self.__query_plan
