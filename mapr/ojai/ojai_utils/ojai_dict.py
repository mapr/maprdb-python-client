from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
class OJAIDict(dict):
    def __init__(self):
        super(OJAIDict, self).__init__()

    @staticmethod
    def parse_dict(value, tags=False):
        if tags:
            from mapr.ojai.ojai.OJAITagsBuilder import OJAITagsBuilder
            dump_document = OJAITagsBuilder()
        else:
            from mapr.ojai.ojai.OJAIDocument import OJAIDocument
            dump_document = OJAIDocument()
        ojai_dict = {}
        for k, v in list(value.items()):
            # this if statement needs for case, when we parsed a dictionary from data access service
            if k in ['$numberLong', '$numberFloat']:
                ojai_dict[k] = v
            else:
                ojai_dict[k] = dump_document.set('dump', v).as_dictionary()['dump']
            dump_document.clear()

        return ojai_dict
