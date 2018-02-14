from mapr.ojai.field_logic.FieldPath import FieldPath
from mapr.ojai.field_logic.Segment import NameSegment


class FieldPathConstant(object):

    empty = FieldPath(NameSegment(name="", quoted=False, child=None))
