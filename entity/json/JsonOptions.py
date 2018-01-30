class JsonOptions:

    """This class encapsulates various options to configure a JSON serializer for Documents.
    Currently, it supports the following options:
        Pretty Print: off by default.
        With Tags: on by default"""

    __pretty = False
    __with_tags = False

    def __init__(self):
        pass

    def is_pretty(self):
        return self.__pretty

    # TODO test it careful
    def __check_mutation_of_constants(self):
        if Options.DEFAULT == self or Options.WITH_TAGS == self:
            raise AttributeError

    def set_pretty(self, pretty):
        self.__check_mutation_of_constants()
        self.__pretty = pretty
        return self

    def pretty(self):
        self.__check_mutation_of_constants()
        self.__pretty = True
        return self

    # TODO deprecated???
    def compact(self):
        self.__check_mutation_of_constants()
        self.__pretty = False
        return self

    def is_with_tags(self, with_tags):
        self.__check_mutation_of_constants()
        self.__with_tags = with_tags
        return self

    def with_tags(self):
        self.__check_mutation_of_constants()
        self.__with_tags = True
        return self

    def without_tags(self):
        self.__check_mutation_of_constants()
        self.__with_tags = False
        return self

    def __str__(self):
        return "\"pretty\"" + self.__pretty + ", \"with_tags\": " + self.__with_tags


class Options:

    def __init__(self):
        pass

    __DEFAULT = JsonOptions()
    __WITH_TAGS = JsonOptions().with_tags()

    @property
    def DEFAULT(self):
        return self.__DEFAULT

    @property
    def WITH_TAGS(self):
        return self.__WITH_TAGS

