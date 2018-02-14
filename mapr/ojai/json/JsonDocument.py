from ojai.document.Document import Document


class JsonDocument(Document):

    __json_stream_document_reader = None

    def __init__(self, json_value=None):
        self.json_value = json_value

    def set_id(self, _id):
        pass

    def get_id(self):
        pass

    def get_id_string(self):
        pass

    def get_id_binary(self):
        pass

    def size(self):
        pass

    def empty(self):
        pass

    def get_id_str(self):
        pass

    def set(self, field_path, value, off=None, length=None):
        pass

    def get_dictionary(self, field_path):
        pass

    def as_dictionary(self):
        pass

    def set_boolean(self, field_path, value):
        pass

    def set_byte(self, field_path, value):
        pass

    def set_long(self, field_path, value):
        pass

    def set_float(self, field_path, value):
        pass

    def set_decimal(self, field_path, value):
        pass

    def set_time(self, field_path, value):
        pass

    def set_date(self, field_path, value):
        pass

    def set_timestamp(self, field_path, value):
        pass

    def set_interval(self, field_path, value):
        pass

    def set_byte_array(self, field_path, value, offset=None, length=None):
        pass

    def set_map(self, field_path, value):
        pass

    def set_document(self, field_path, value):
        pass

    def set_value_obj(self, field_path, value):
        pass

    def set_array(self, field_path, values):
        pass

    def set_null(self, field_path):
        pass

    def delete(self, field_path):
        pass

    def get_string(self, field_path):
        pass

    def get_boolean(self, field_path):
        pass

    def get_byte(self, field_path):
        pass

    def get_int(self, field_path):
        pass

    def get_long(self, field_path):
        pass

    def get_float(self, field_path):
        pass

    def get_double(self, field_path):
        pass

    def get_decimal(self, field_path):
        pass

    def get_time(self, field_path):
        pass

    def get_date(self, field_path):
        pass

    def get_timestamp(self, field_path):
        pass

    def get_binary(self, field_path):
        pass

    def get_interval(self, field_path):
        pass

    def get_value(self, field_path):
        pass

    def get_map(self, field_path):
        pass

    def get_list(self, field_path):
        pass

    def as_reader(self, field_path=None):
        pass

    def as_map(self):
        pass
