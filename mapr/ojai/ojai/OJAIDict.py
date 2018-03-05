class OJAIDict(dict):
    def __init__(self):
        super(OJAIDict, self).__init__()


    @staticmethod
    def parse_dict(value):
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        dump_document = OJAIDocument()
        ojai_dict = {}
        # for k, v in value.iteritems():
        #     if isinstance(v, dict):
        #         OJAIDict.parse_dict(v)

        for k, v in value.iteritems():
            # if isinstance(v, list):
            #     ojai_list.append({k: OJAIDict.set_list(v)})
            # else:
            #     internal_value = dump_document.set('dump', v).as_dictionary()['dump']
            #     ojai_list.append({k: internal_value})
            ojai_dict[k] = dump_document.set('dump', v).as_dictionary()['dump']
            dump_document.clear()

        return ojai_dict

    @staticmethod
    def set_list(value):
        ojai_list = []
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        dump_document = OJAIDocument()

        for elem in value:
            if isinstance(elem, list):
                nested_list = OJAIDict.set_list(elem)
                ojai_list.append(nested_list)
            elif isinstance(elem, dict) and bool(elem):
                for k, v in elem.iteritems():
                    if isinstance(v, list):
                        ojai_list.append({k: OJAIDict.set_list(v)})
                    else:
                        internal_value = dump_document.set('dump', v).as_dictionary()['dump']
                        ojai_list.append({k: internal_value})
            else:
                ojai_list.append(dump_document.set('dump', elem).as_dictionary()['dump'])
            dump_document.clear()
        return ojai_list
