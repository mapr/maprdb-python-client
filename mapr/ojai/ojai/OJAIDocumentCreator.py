import json

from mapr.ojai.ojai.OJAIDocument import OJAIDocument


class OJAIDocumentCreator:

    def __init__(self):
        pass

    @staticmethod
    def create_document(json_string, tags=True):
        parsed_dict = json.loads(json_string)
        doc = OJAIDocument()
        if tags:
            for k, v in parsed_dict.iteritems():
                doc.set(k, v)
        return doc
