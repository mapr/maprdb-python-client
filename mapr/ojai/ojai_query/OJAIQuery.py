from ojai.store.Query import Query


class OJAIQuery(Query):
    def set_option(self, option_name, value=None):
        pass

    def set_options(self, options):
        pass

    def set_timeout(self, timeout_in_millis):
        pass

    def select(self, field_paths):
        pass

    def where(self, condition):
        pass

    def order_by(self, field_paths, order=None):
        pass

    def offset(self, offset):
        pass

    def limit(self, limit):
        pass

    def build(self):
        pass
