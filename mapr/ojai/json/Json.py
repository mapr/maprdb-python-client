from mapr.ojai.json import JsonDocument

from mapr.ojai.json.JsonDocumentStream import JsonDocumentStream
from mapr.ojai.json.JsonOptions import Options


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
            # TODO  JsonDocumentStream required!!! iterator impl
            return Json.new_document_stream(input_stream=byte_array).iterator()
        elif json_map is not None and type(json_map) is map:
            # TODO JsonValueBuilder required
            # TODO not required for init release
            pass
        else:
            raise AttributeError

    # @staticmethod
    # def get_value_builder():
    #     """Returns a ValueBuilder object."""
    #     # TODO added implementation after JsonValueBuilder was added.
    #     pass

    @staticmethod
    def new_document_reader(json_string):
        """Returns a new instance of the JSON DocumentReader."""
        byte_array = bytearray(json_string)
        # todo JsonDocumentStream required !!! iterator impl
        return Json.new_document_stream(input_stream=byte_array).iterator()

    # @staticmethod
    # def new_document_builder(options=None):
    #     """Returns a new instance of JSON DocumentBuilder."""
    #     if options is None:
    #         return JsonDocumentBuilder()
    #     else:
    #         # todo required JsonDocumentBuilder, options!!
    #         pass

    @staticmethod
    def new_document_stream(input_stream=None, field_path_type_map=None, event_delegate=None,
                            fs=None, path=None):
        # TODO
        if fs is None and path is None:
            return JsonDocumentStream(input_stream=input_stream,
                                      field_path_type_map=field_path_type_map,
                                      event_delegate=event_delegate)
        elif fs is not None and path is not None:
            return JsonDocumentStream.new_document_stream(fs=fs, path=path,
                                                          field_path_type_map=field_path_type_map,
                                                          event_delegate=event_delegate)
        else:
            raise AttributeError("Unexpected input params set")

    # TODO encode method skipped, bean required

    @staticmethod
    def to_json_string(document=None, options=None, document_reader=None):
        if document is not None:
            document_reader = document.as_reader()

        if options is None:
            options = Options.DEFAULT
        # TODO JsonDocumentBuilder and DocumentReader required!!!

    # @staticmethod
    # def write_reader_to_builder(document_reader, document_builder):
    #     Documents.write_reader_to_builder(document_reader=document_reader, document_builder=document_builder)
