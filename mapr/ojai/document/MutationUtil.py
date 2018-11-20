from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
class MutationUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def evaluate_common(path, value, operation_type, mutation_dict, doc):
        if operation_type.value in mutation_dict:
            values = mutation_dict[operation_type.value]
            if not isinstance(values, list):
                values = [values]
            for mutate_value in values:
                if path in mutate_value:
                    mutate_value[path] = doc.set(operation_type.value, value).as_dictionary()[operation_type.value]
                    return mutation_dict
            values.append({path: doc.set(operation_type.value, value).as_dictionary()[operation_type.value]})
        else:
            values = {path: doc.set(operation_type.value, value).as_dictionary()[operation_type.value]}

        mutation_dict[operation_type.value] = values
        doc.clear()
        return mutation_dict

    @staticmethod
    def append(path, value):
        pass

    @staticmethod
    def merge(path, value, operation_type, mutation_dict, doc):
        if operation_type.value in mutation_dict:
            values = mutation_dict[operation_type.value]
            for mutate_value in values:
                if path in mutate_value:
                    mutate_value[path] = doc.set(operation_type.value, value).as_dictionary()[operation_type.value]
                    return mutation_dict
            values.append({path: doc.set(operation_type.value, value).as_dictionary()[operation_type.value]})
        else:
            values = [{path: doc.set(operation_type.value, value).as_dictionary()[operation_type.value]}]

        mutation_dict[operation_type.value] = values
        doc.clear()
        return mutation_dict

    @staticmethod
    def delete(path, mutation_dict, operation_type, doc):
        if operation_type.value in mutation_dict:
            values = mutation_dict[operation_type.value]
            if not isinstance(values, list):
                values = [values]
            if path in values:
                return mutation_dict
            else:
                values.append(path)
        else:
            values = path

        mutation_dict[operation_type.value] = values
        doc.clear()
        return mutation_dict

