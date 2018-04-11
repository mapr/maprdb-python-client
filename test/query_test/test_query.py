from __future__ import unicode_literals

import json

from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
# from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition, _is
# from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.ojai_query.QueryOp import QueryOp

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class QueryTest(unittest.TestCase):

    def test_simple_query(self):
        query = OJAIQuery().select([True, 5, 123123124123]).build()

        self.assertEqual(query.query_dict(), {'$select': ['True', '5', '123123124123']})

    def test_condition(self):
        query_condition = OJAIQueryCondition() \
            .and_() \
            .is_('age', QueryOp.GREATER_OR_EQUAL, 18) \
            .is_('city', QueryOp.EQUAL, 'London').close().close()

        query_condition.build()
        self.assertEqual(query_condition.as_dictionary(),
                         {'$and': [{'$ge': {'age': 18}}, {'$eq': {'city': 'London'}}]})

    def test_multiple_and(self):
        qc = OJAIQueryCondition() \
            .and_() \
            .and_() \
            .is_(field_path='age', op=QueryOp.GREATER_OR_EQUAL, value=18) \
            .is_(field_path='city', op=QueryOp.EQUAL, value='London') \
            .close() \
            .and_() \
            .is_(field_path='age', op=QueryOp.GREATER_OR_EQUAL, value=22) \
            .is_(field_path='city', op=QueryOp.EQUAL, value='NY') \
            .close() \
            .close()

        qc.build()

        self.assertEqual(qc.as_dictionary(), {'$and': [
            {'$and': [
                {'$ge': {'age': 18}},
                {'$eq': {'city': 'London'}}]},
            {'$and': [
                {'$ge': {'age': 22}},
                {'$eq': {'city': 'NY'}}]}
        ]})

    def test_and_with_separate_is(self):
        qc = OJAIQueryCondition() \
            .and_() \
            .and_() \
            .is_(field_path='age', op=QueryOp.GREATER_OR_EQUAL, value=18) \
            .is_(field_path='city', op=QueryOp.EQUAL, value='London') \
            .close() \
            .and_() \
            .is_(field_path='age', op=QueryOp.GREATER_OR_EQUAL, value=22) \
            .is_(field_path='city', op=QueryOp.EQUAL, value='NY') \
            .close() \
            .is_('card', QueryOp.EQUAL, 'visa') \
            .close()

        qc.build()

        self.assertEqual(qc.as_dictionary(), {'$and': [
            {'$and': [
                {'$ge': {'age': 18}},
                {'$eq': {'city': 'London'}}]},
            {'$and': [
                {'$ge': {'age': 22}},
                {'$eq': {'city': 'NY'}}]},
            {'$eq': {'card': 'visa'}}
        ]})

    def test_nested_and(self):
        qc = OJAIQueryCondition().and_() \
            .is_(field_path='card', op=QueryOp.NOT_EQUAL, value="visa") \
            .or_() \
            .is_(field_path='age', op=QueryOp.GREATER_OR_EQUAL, value=22) \
            .is_(field_path='city', op=QueryOp.EQUAL, value='NY') \
            .and_() \
            .is_(field_path='age', op=QueryOp.GREATER_OR_EQUAL, value=18) \
            .is_(field_path='city', op=QueryOp.EQUAL, value='London').close().close().close().build()

        self.assertEqual(qc.as_dictionary(), {'$and': [
            {'$ne': {u'card': u'visa'}},
            {'$or': [
                {'$ge': {u'age': 22}},
                {'$eq': {u'city': u'NY'}},
                {'$and': [
                    {'$ge': {u'age': 18}},
                    {'$eq': {u'city': u'London'}}
                ]}
            ]}
        ]})

    def test_eq_condition(self):
        qc = OJAIQueryCondition().and_().not_equals_('name', 'Joh').equals_('name', 'David').close().build()
        self.assertEqual(qc.as_dictionary(), {'$and': [{'$ne': {'name': 'Joh'}}, {'$eq': {'name': 'David'}}]})

    def test_nested_condition(self):
        qc = OJAIQueryCondition().and_() \
            .condition_(condition_to_add=OJAIQueryCondition()
                        .or_()
                        .is_(field_path='age', op=QueryOp.GREATER_OR_EQUAL, value=22)
                        .is_(field_path='city', op=QueryOp.EQUAL, value='NY').close()) \
            .condition_(condition_to_add=OJAIQueryCondition()
                        .and_()
                        .is_(field_path='age', op=QueryOp.GREATER_OR_EQUAL, value=18)
                        .is_(field_path='city', op=QueryOp.EQUAL, value='London').close())

        qc.close().build()

        self.assertEqual(qc.as_dictionary(), {'$and': [
            {'$or': [
                {'$ge': {u'age': 22}},
                {'$eq': {u'city': u'NY'}}]},
            {'$and': [
                {'$ge': {u'age': 18}},
                {'$eq': {u'city': u'London'}}]}
        ]})

    def test_full_query(self):
        qc = OJAIQueryCondition().and_() \
            .condition_(OJAIQueryCondition()
                        .or_()
                        .is_('age', QueryOp.GREATER_OR_EQUAL, 22)
                        .is_('city', QueryOp.EQUAL, 'NY').close()) \
            .condition_(OJAIQueryCondition()
                        .and_()
                        .is_('age', QueryOp.GREATER_OR_EQUAL, 18)
                        .is_('city', QueryOp.EQUAL, 'London').close()).close().build()

        query = OJAIQuery().select(['name', 'age', 'city']).where(qc).order_by('name').offset(500).limit(5).build()

        self.assertEqual(query.query_dict(), {'$orderby': {'name': 'asc'},
                                              '$offset': 500,
                                              '$select': ['name', 'age', 'city'],
                                              '$limit': 5,
                                              '$where': {'$and': [
                                                  {'$or': [
                                                      {'$ge': {'age': 22}},
                                                      {'$eq': {'city': 'NY'}}]},
                                                  {'$and': [
                                                      {'$ge': {'age': 18}},
                                                      {'$eq': {'city': 'London'}}
                                                  ]}
                                              ]}})

    def test_query_check_existing_condition(self):
        qc = OJAIQueryCondition().is_('age', QueryOp.GREATER_OR_EQUAL, 55).is_('age', QueryOp.GREATER_OR_EQUAL, 18) \
            .close().build()
        self.assertEqual(qc.as_dictionary(), {'$ge': {'age': 18}})

    def test_query_condition_multiple_is(self):
        qc = OJAIQueryCondition().is_('age', QueryOp.GREATER_OR_EQUAL, 55).is_('age', QueryOp.NOT_EQUAL, 18) \
            .close().build()
        self.assertEqual(qc.as_dictionary(), {'$ge': {'age': 55}, '$ne': {'age': 18}})

    def test_in_condition(self):
        qc = OJAIQueryCondition().in_('age', [20, 21, 22, 23, 24, 25]).close().build()

        self.assertEqual(qc.as_dictionary(), {'$in': {'age': [20, 21, 22, 23, 24, 25]}})

    def test_not_in_condition(self):
        qc = OJAIQueryCondition().not_in_('age', [20, 21, 22, 23, 24, 25]).close().build()
        self.assertEqual(qc.as_dictionary(), {'$notin': {'age': [20, 21, 22, 23, 24, 25]}})

    def test_exists(self):
        qc = OJAIQueryCondition().exists_('city').close().build()
        self.assertEqual(qc.as_dictionary(), {'$exists': 'city'})

    def test_not_exists(self):
        qc = OJAIQueryCondition().not_exists_('city').close().build()
        self.assertEqual(qc.as_dictionary(), {'$notexists': 'city'})

    def test_like(self):
        qc = OJAIQueryCondition().like_('card', 'visa').close().build()
        self.assertEqual(qc.as_dictionary(), {'$like': {'card': 'visa'}})

    def test_not_like(self):
        qc = OJAIQueryCondition().not_like_('card', 'visa').close().build()
        self.assertEqual(qc.as_dictionary(), {'$notlike': {'card': 'visa'}})

    def test_empty_condition(self):
        qc = OJAIQueryCondition()
        self.assertTrue(qc.is_empty())

        qc.is_('name', QueryOp.EQUAL, 'Doe').close()
        self.assertTrue(qc.is_empty())

        qc.build()
        self.assertFalse(qc.is_empty())

    def test_order_by(self):
        query = OJAIQuery().order_by('name').build()

        self.assertEqual(query.query_dict(), {'$orderby': {'name': 'asc'}})

        query2 = OJAIQuery().order_by(['name', 'age']).build()

        self.assertEqual(query2.query_dict(), {'$orderby': [{'name': 'asc'}, {'age': 'asc'}]})

        query3 = OJAIQuery().order_by(['address.city', 'address.postal_code'], 'desc').build()

        self.assertEqual(query3.query_dict(), {'$orderby': [{'address.city': 'desc'}, {'address.postal_code': 'desc'}]})

    def test_empty_query(self):
        query = OJAIQuery().build()
        self.assertEqual(query.query_dict(), {})
        self.assertEqual(query.to_json_str(), '{}')

    def test_limit_bool(self):
        with self.assertRaises(TypeError):
            query = OJAIQuery().limit(True).build()

    def test_offset_bool(self):
        with self.assertRaises(TypeError):
            query = OJAIQuery().offset(True).build()

    def test_where_dict(self):
        query = OJAIQuery().where({'$ne': {'name': 'Joh'}}).build()
        self.assertEqual({'$where': {'$ne': {'name': 'Joh'}}}, query.query_dict())

    def test_where_json_str(self):
        query = OJAIQuery().where("{\"$eq\": {\"address.zipCode\": 95196}}").build()
        self.assertEqual({'$where': {'$eq': {'address.zipCode': 95196}}}, query.query_dict())

    def test_where_json_str_format(self):
        query = OJAIQuery().where("{\"$eq\": {\"address.zipCode\": 95196}}").build()
        self.assertEqual('{"$where": {"$eq": {"address.zipCode": 95196}}}', query.to_json_str())

    def test_empty_where(self):
        with self.assertRaises(AttributeError):
            query = OJAIQuery().where({}).build()

        with self.assertRaises(AttributeError):
            query = OJAIQuery().where('').build()

        with self.assertRaises(AttributeError):
            query = OJAIQuery().where(u'').build()

        with self.assertRaises(AttributeError):
            query = OJAIQuery().where(OJAIQueryCondition().build()).build()

    def test_order_by_empty(self):
        with self.assertRaises(TypeError):
            query = OJAIQuery().order_by([]).build()

        with self.assertRaises(TypeError):
            query = OJAIQuery().order_by('').build()
