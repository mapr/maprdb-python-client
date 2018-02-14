from mapr.ojai.antrl4.FieldPathLexer import FieldPathLexer
from mapr.ojai.antrl4.FieldPathParser import FieldPathParser
from mapr.ojai.field_logic.FieldPath import FieldPath
from antlr4.InputStream import InputStream

from mapr.ojai.field_logic.FieldPathConstant import FieldPathConstant
from mapr.ojai.field_logic.Segment import NameSegment
from antlr4 import *


class FieldParser():
    @staticmethod
    def parse_from(field_path):
        """
        Parse and create FieldPath object from string path representation.
        :param field_path: represented as string
        :return: FieldPath obj
        """

        if not isinstance(field_path, str) and not isinstance(field_path, unicode) or field_path is None:
            raise TypeError
        elif len(str(field_path)) == 0:
            # return FieldPath(NameSegment(name="", quoted=False, child=None))
            """:return Empty instance of NameSegment"""
            return FieldPathConstant.empty
        stream = InputStream(field_path)
        lexer = FieldPathLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = FieldPathParser(token_stream)

        fp = parser.parse().fp

        return FieldPathConstant.empty if FieldPathConstant.empty.__eq__(fp) else fp
