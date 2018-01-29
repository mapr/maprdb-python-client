from entity.json import JsonDocument

from entity.json.JsonDocumentBuilder import JsonDocumentBuilder


class Json:
    def __init__(self):
        pass

    @staticmethod
    def new_document(json_string=None, json_map=None):
        """Returns a new, empty Document or from the specified JSON string or map."""
        if json_string is None and json_map is None:
            return JsonDocument()
        elif json_string is not None and type(json_string) is str:
            byte_array = bytearray(json_string)
            # TODO  newDocumentStream required
            pass
        elif json_map is not None and type(json_map) is map:
            # TODO JsonValueBuilder required
            pass
        else:
            raise TypeError

    @staticmethod
    def get_value_builder():
        """Returns a ValueBuilder object."""
        # TODO added implementation after JsonValueBuilder was added.
        pass

    @staticmethod
    def new_document_reader(json_string):
        """Returns a new instance of the JSON DocumentReader."""
        byte_array = bytearray(json_string)
        # todo newDocumentStream required

    @staticmethod
    def new_document_builder(options=None):
        """Returns a new instance of JSON DocumentBuilder."""
        if options is None:
            return JsonDocumentBuilder()
        else:
            # todo required JsonDocumentBuilder
            pass

    @staticmethod
    def new_document_stream(input_stream=None, field_path_type_map=None, event_delegate=None,
                            fs=None, path=None):
        # TODO
        pass
