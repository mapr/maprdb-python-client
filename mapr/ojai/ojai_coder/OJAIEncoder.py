from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.proto.gen.ojai_pb2 import DocumentPayload


class OJAIEncoder:
    def __init__(self):
        pass

    @staticmethod
    def encode(doc):
        pass

    @staticmethod
    def decode(doc_payload):
        documents = doc_payload.documents
        decoded_documents = []
        for doc in documents:
            decoded_doc = OJAIDocument()
            for k, v in doc.key_value.iteritems():
                decoded_doc.set(k, v)
            decoded_documents.append(decoded_doc)

        return decoded_documents

