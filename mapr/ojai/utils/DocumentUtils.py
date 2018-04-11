from copy import deepcopy

import re


class DocumentUtils:
    __regex = re.compile(r"""(["']).*?\1|(?P<dot>\.)""")

    def __init__(self):
        pass

    @staticmethod
    def merge_two_dicts(dict1, dict2):
        if not isinstance(dict2, dict):
            return dict2
        merged_dict = deepcopy(dict1)
        for k, v in dict2.iteritems():
            if k in merged_dict and isinstance(merged_dict[k], dict):
                merged_dict[k] = DocumentUtils.merge_two_dicts(merged_dict[k], v)
            elif k in merged_dict and isinstance(merged_dict[k], list):
                swap = False
                for dict_element in merged_dict[k]:
                    for elem_k in dict_element:
                        if isinstance(v, list):
                            for item in v:
                                if elem_k in item:
                                    index = merged_dict[k].index(dict_element)
                                    merged_dict[k].remove(dict_element)
                                    merged_dict[k].insert(index, item)
                                    swap = True
                        else:
                            if elem_k in v:
                                index = merged_dict[k].index(dict_element)
                                merged_dict[k].remove(dict_element)
                                merged_dict[k].insert(index, v)
                                swap = True
                if not swap:
                    merged_dict[k].append(v)
            else:
                merged_dict[k] = deepcopy(v)
        return merged_dict

    @staticmethod
    def __replacer(match):
        if match.group('dot') is not None:
            return "pass"
        else:
            return match.group(0)

    @staticmethod
    def __parse_list(values_list):
        from mapr.ojai.ojai.OJAIDocument import OJAIDocument
        temp_doc = OJAIDocument()
        parsed_list = []
        for element in values_list:
            temp_doc.set('parse_list', element)
            parsed_list.append(temp_doc.as_dictionary()['parse_list'])

        return parsed_list

    @staticmethod
    def __parse_field_path(field_path, value, oja_type=None):
        split_path = [part.strip("'").strip('"')
                      for part in DocumentUtils.__regex.sub(DocumentUtils.__replacer,
                                                            field_path).split("pass") if part]
        tmp_dict = {}

        for i in reversed(split_path):
            if tmp_dict == {}:
                if oja_type is None:
                    tmp_dict = {i: value}
                else:
                    tmp_dict = {i: {oja_type: value}}
            else:
                tmp_dict = {i: tmp_dict}

        return tmp_dict
