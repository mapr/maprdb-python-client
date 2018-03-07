class OJAIDict(dict):
    def __init__(self):
        super(OJAIDict, self).__init__()

    @staticmethod
    def parse_dict(value):
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        dump_document = OJAIDocument()
        ojai_dict = {}

        for k, v in value.iteritems():
            ojai_dict[k] = dump_document.set('dump', v).as_dictionary()['dump']
            dump_document.clear()

        return ojai_dict
