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
        for k, v in value.iteritems():
            # this if statement needs for case, when we parsed a dictionary from data access service
            if k in ['$numberLong', '$numberFloat']:
                ojai_dict[k] = v
            else:
                ojai_dict[k] = dump_document.set('dump', v).as_dictionary()['dump']
            dump_document.clear()

        return ojai_dict
