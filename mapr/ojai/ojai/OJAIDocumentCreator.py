import json

from copy import deepcopy

from mapr.ojai.ojai.OJAIDocument import OJAIDocument


class OJAIDocumentCreator:

    def __init__(self):
        pass

    @staticmethod
    def create_document(json_string):
        parsed_dict = json.loads(json_string)
        return OJAIDocument().from_dict(OJAIDocumentCreator.remove_tags(parsed_dict))

    @staticmethod
    def remove_tags(tags_dict):
        result_dict = {}

        for key, value in tags_dict.iteritems():
            if isinstance(value, dict):
                result_dict[key] = OJAIDocumentCreator.remove_tags(value)
            elif isinstance(value, list):
                result_dict[key] = OJAIDocumentCreator.clear_list(value)
            elif key in ('$numberLong', '$numberFloat', '$numberShort', '$decimal'):
                return value
            elif key == '$binary':
                return bytearray(value, 'ISO-8859-1')
            elif key in ('$interval', '$date', '$dateDay', '$time'):
                return OJAIDocumentCreator.generate_o_types(key, value)
            else:
                result_dict[key] = value
        return result_dict

    @staticmethod
    def clear_list(list_value):
        result_list = []
        for element in list_value:
            if isinstance(element, dict):
                result_list.append(OJAIDocumentCreator.remove_tags(element))
            elif isinstance(element, list):
                result_list.append(OJAIDocumentCreator.clear_list(element))
            else:
                result_list.append(element)
        return result_list

    @staticmethod
    def generate_o_types(str_type, str_value):
        if str_type == '$interval':
            from ojai.o_types.OInterval import OInterval
            return OInterval(milli_seconds=str_value)
        elif str_type == '$date':
            from ojai.o_types.OTimestamp import OTimestamp
            return OTimestamp.parse(str_value)
        elif str_type == '$dateDay':
            from ojai.o_types.ODate import ODate
            return ODate.parse(str_value)
        else:
            from ojai.o_types.OTime import OTime
            return OTime.parse(str_value)

