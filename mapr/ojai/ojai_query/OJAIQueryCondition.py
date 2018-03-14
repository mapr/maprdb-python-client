from ojai.store.QueryCondition import QueryCondition


class OJAIQueryCondition(QueryCondition):
    def is_empty(self):
        pass

    def is_built(self):
        pass

    def _and(self):
        pass

    def _or(self):
        pass

    def close(self):
        pass

    def build(self):
        pass

    def _condition(self, condition_to_add):
        pass

    def _exists(self, field_path):
        pass

    def _not_exists(self, field_path):
        pass

    def _in(self, field_path, list_of_value):
        pass

    def _not_in(self, field_path, list_of_value):
        pass

    def _type_of(self, field_path, value_type):
        pass

    def _not_type_of(self, field_path, value_type):
        pass

    def _matches(self, field_path, regex):
        pass

    def _not_matches(self, field_path, regex):
        pass

    def _like(self, field_path, like_expression, escape_char=None):
        pass

    def _not_like(self, field_path, like_expression, escape_char=None):
        pass

    def _is(self, field_path, op, value):
        pass

    def _equals(self, field_path, value):
        pass

    def _not_equals(self, field_path, value):
        pass

    def _size_of(self, field_path, op, size):
        pass