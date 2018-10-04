from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from mapr.ojai.document.OJAIDocumentMutation import OJAIDocumentMutation
from mapr.ojai.exceptions.IllegalArgumentError import IllegalArgumentError

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DocumentMutationTest(unittest.TestCase):

    def test_document_mutation_set(self):
        doc_mutation = OJAIDocumentMutation().set('a.b.c', 50)
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50}})
        doc_mutation.set('g', 12)
        self.assertEqual(doc_mutation.as_dict(), {'$set': [{'a.b.c': 50},
                                                           {'g': 12}]})

        doc_mutation.set('a.b.c', 'another_type')
        self.assertEqual(doc_mutation.as_dict(),
                         {'$set': [{'a.b.c': 'another_type'},
                                   {'g': 12}]})

    def test_document_mutation_empty(self):
        doc_mutation = OJAIDocumentMutation().set('a.b.c', 50)
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50}})
        doc_mutation.empty()
        self.assertEqual(doc_mutation.as_dict(), {})

    def test_document_mutation_set_or_replace(self):
        doc_mutation = OJAIDocumentMutation().set('a.b.c', 50)
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50}})
        doc_mutation.set_or_replace('q.s.d', '55')
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50},
                                                  '$put': {'q.s.d': '55'}})
        doc_mutation.set_or_replace('p.o.t', 55)
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50},
                                                  '$put': [{'q.s.d': '55'},
                                                           {'p.o.t': 55}]})
        doc_mutation.set_or_replace('q.s.d', False)
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50},
                                                  '$put': [{'q.s.d': False},
                                                           {'p.o.t': 55}]})

    def test_document_mutation_delete(self):
        doc_mutation = OJAIDocumentMutation().set('a.b.c', 50)
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50}})
        doc_mutation.delete('q.s.d')
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50},
                                                  '$delete': 'q.s.d'})
        doc_mutation.delete('s.a.b')
        self.assertEqual(doc_mutation.as_dict(), {'$set': {'a.b.c': 50},
                                                  '$delete': ['q.s.d',
                                                              's.a.b']})

    def test_document_mutation_merge(self):
        doc_mutation = OJAIDocumentMutation().merge('a.b.c',
                                                    {'d': 55, 'g': 'text'})
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}}})
        doc_mutation.set_or_replace('kon', 'ek')
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}},
                          '$put': {'kon': 'ek'}})
        doc_mutation.empty()
        self.assertEqual(doc_mutation.as_dict(), {})

    def test_document_mutation_append(self):
        doc_mutation = OJAIDocumentMutation().merge('a.b.c',
                                                    {'d': 55, 'g': 'text'})
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}}})
        doc_mutation.set_or_replace('kon', 'ek')
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}},
                          '$put': {'kon': 'ek'}})
        doc_mutation.append('w.e', [1, False])
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}},
                          '$put': {'kon': 'ek'},
                          '$append': {'w.e': [1, False]}})
        doc_mutation.append('t.g', ['hello', 66, False])
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}},
                          '$put': {'kon': 'ek'},
                          '$append': [{'w.e': [1, False]},
                                      {'t.g': ['hello', 66, False]}]})
        doc_mutation.empty()
        self.assertEqual(doc_mutation.as_dict(), {})

    def test_document_mutation_increment(self):
        doc_mutation = OJAIDocumentMutation().merge('a.b.c',
                                                    {'d': 55, 'g': 'text'})
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}}})
        doc_mutation.increment('b', 5)
        doc_mutation.increment('a.w', 66)
        self.assertEqual(doc_mutation.as_dict(),
                         {'$increment': [{'b': 5},
                                         {'a.w': 66}],
                          '$merge': {'a.b.c': {'d': 55, 'g': 'text'}}})

    def test_document_mutation_decrement(self):
        doc_mutation = OJAIDocumentMutation().merge('a.b.c',
                                                    {'d': 55, 'g': 'text'})
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}}})
        doc_mutation.decrement('b', 5)
        doc_mutation.decrement('a.w', 66)
        self.assertEqual(doc_mutation.as_dict(),
                         {'$decrement': [{'b': 5},
                                         {'a.w': 66}],
                          '$merge': {'a.b.c': {'d': 55, 'g': 'text'}}})
        doc_mutation.decrement('hhh')
        self.assertEqual(doc_mutation.as_dict(),
                         {'$decrement': [{'b': 5},
                                         {'a.w': 66},
                                         {'hhh': 1}],
                          '$merge': {'a.b.c': {'d': 55, 'g': 'text'}}})

    def test_document_mutation_set_arr(self):
        doc_mutation = OJAIDocumentMutation() \
            .set('a.b[0].boolean', True)
        self.assertEqual({"$set": {"a.b[0].boolean": True}},
                         doc_mutation.as_dict())
        doc_mutation.set('a.c.d', 11) \
            .set('a.x', 1)
        self.assertEqual(
            {"$set": [{"a.b[0].boolean": True}, {"a.c.d": 11}, {"a.x": 1}]},
            doc_mutation.as_dict())

    def test_document_mutation_put(self):
        doc_mutation = OJAIDocumentMutation() \
            .set_or_replace('a.b[0].boolean', True) \
            .set_or_replace('a.c.d', 'eureka') \
            .set_or_replace('a.x', 1)
        self.assertEqual({"$put": [{"a.b[0].boolean": True},
                                   {"a.c.d": 'eureka'}, {"a.x": 1}]},
                         doc_mutation.as_dict())

    def test_document_mutation_delete_arr(self):
        doc_mutation = OJAIDocumentMutation() \
            .delete('a.b[1]')
        self.assertEqual({'$delete': 'a.b[1]'}, doc_mutation.as_dict())
        doc_mutation.delete('a.c.e')
        self.assertEqual({'$delete': ['a.b[1]', 'a.c.e']},
                         doc_mutation.as_dict())

    def test_document_mutation_increment_doc_example(self):
        doc_mutation = OJAIDocumentMutation().increment('a.c.d', -5)
        self.assertEqual({'$increment': {'a.c.d': -5}}, doc_mutation.as_dict())
        doc_mutation.increment('q.w.e', 11)
        self.assertEqual({'$increment': [{'a.c.d': -5}, {'q.w.e': 11}]},
                         doc_mutation.as_dict())

    def test_document_mutation_decrement_doc_example(self):
        doc_mutation = OJAIDocumentMutation().decrement('a.c.d', 5)
        self.assertEqual({'$decrement': {'a.c.d': 5}}, doc_mutation.as_dict())
        doc_mutation.decrement('q.w.e', 11)
        self.assertEqual({'$decrement': [{'a.c.d': 5}, {'q.w.e': 11}]},
                         doc_mutation.as_dict())

    def test_document_mutation_append_doc_example(self):
        doc_mutation = OJAIDocumentMutation().append('a.b', [{'appd': 1}])
        self.assertEqual({'$append': {'a.b': [{'appd': 1}]}},
                         doc_mutation.as_dict())
        doc_mutation.append('a.c.e', 'MapR')
        self.assertEqual(
            {'$append': [{'a.b': [{'appd': 1}]}, {'a.c.e': 'MapR'}]},
            doc_mutation.as_dict())

    def test_document_mutation_multiple_merge(self):
        doc_mutation = OJAIDocumentMutation().merge('a.b.c',
                                                    {'d': 55, 'g': 'text'})
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': {'a.b.c': {'d': 55, 'g': 'text'}}})
        doc_mutation.merge('t.o.y', {'b': 9, 'o': 1, 'y': 1})
        self.assertEqual(doc_mutation.as_dict(),
                         {'$merge': [{'a.b.c': {'d': 55, 'g': 'text'}},
                                     {'t.o.y': {'b': 9, 'o': 1, 'y': 1}}]})

    def test_invalid_with_path(self):
        with self.assertRaises(IllegalArgumentError):
            OJAIDocumentMutation().set('_id', 5)
        with self.assertRaises(IllegalArgumentError):
            OJAIDocumentMutation().set_or_replace('_id', 5)
        with self.assertRaises(IllegalArgumentError):
            OJAIDocumentMutation().delete('_id')
        with self.assertRaises(IllegalArgumentError):
            OJAIDocumentMutation().increment(field_path='_id')
        with self.assertRaises(IllegalArgumentError):
            OJAIDocumentMutation().decrement('_id')
        with self.assertRaises(IllegalArgumentError):
            OJAIDocumentMutation().append('_id', ['1', '2', '3'])
        with self.assertRaises(IllegalArgumentError):
            OJAIDocumentMutation().merge(field_path='_id', value={'a': 5})

    def test_document_mutation_increment_decrement_bool(self):
        with self.assertRaises(TypeError):
            OJAIDocumentMutation().increment('test_increment', True)
        with self.assertRaises(TypeError):
            OJAIDocumentMutation().decrement('test_decrement', True)
