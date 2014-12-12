import json
import unittest
from addict import Dict

TEST_VAL = [1, 2, 3]
TEST_DICT = {'a': {'b': {'c': TEST_VAL}}}
TEST_DICT_STR = str(TEST_DICT)

class Tests(unittest.TestCase):

    def test_set_one_level_item(self):
        some_dict = {'a': TEST_VAL}
        prop = Dict()
        prop['a'] = TEST_VAL
        self.assertDictEqual(prop, some_dict)

    def test_set_two_level_items(self):
        some_dict = {'a': {'b': TEST_VAL}}
        prop = Dict()
        prop['a']['b'] = TEST_VAL
        self.assertDictEqual(prop, some_dict)

    def test_set_three_level_items(self):
        prop = Dict()
        prop['a']['b']['c'] = TEST_VAL
        self.assertDictEqual(prop, TEST_DICT)

    def test_set_one_level_property(self):
        prop = Dict()
        prop.a = TEST_VAL
        self.assertDictEqual(prop, {'a': TEST_VAL})

    def test_set_two_level_properties(self):
        prop = Dict()
        prop.a.b = TEST_VAL
        self.assertDictEqual(prop, {'a': {'b': TEST_VAL}})

    def test_set_three_level_properties(self):
        prop = Dict()
        prop.a.b.c = TEST_VAL
        self.assertDictEqual(prop, TEST_DICT)

    def test_instantiation(self):
        self.assertDictEqual(TEST_DICT, Dict(TEST_DICT))

    def test_getitem(self):
        prop = Dict(TEST_DICT)
        self.assertEqual(prop['a']['b']['c'], TEST_VAL)

    def test_getattr(self):
        prop = Dict(TEST_DICT)
        self.assertEqual(prop.a.b.c, TEST_VAL)

    def test_isinstance(self):
        self.assertTrue(isinstance(Dict(), dict))

    def test_str(self):
        prop = Dict(TEST_DICT)
        self.assertEqual(str(prop), str(TEST_DICT))

    def test_json(self):
        some_dict = TEST_DICT
        some_json = json.dumps(some_dict)
        prop = Dict()
        prop.a.b.c = TEST_VAL
        prop_json = json.dumps(prop)
        self.assertEqual(some_json, prop_json)

    def test_delitem(self):
        prop = Dict({'a': 2})
        del prop['a']
        self.assertDictEqual(prop, {})

    def test_delitem_nested(self):
        prop = Dict(TEST_DICT)
        del prop['a']['b']['c']
        self.assertDictEqual(prop, {'a': {'b': {}}})

    def test_delattr(self):
        prop = Dict({'a': 2})
        del prop.a
        self.assertDictEqual(prop, {})

    def test_delattr_nested(self):
        prop = Dict(TEST_DICT)
        del prop.a.b.c
        self.assertDictEqual(prop, {'a': {'b': {}}})

    def test_delitem_delattr(self):
        prop = Dict(TEST_DICT)
        del prop.a['b']
        self.assertDictEqual(prop, {'a': {}})

    def test_prune(self):
        prop = Dict()
        prop.a.b.c.d
        prop.b
        prop.c = 2
        prop.prune()
        self.assertDictEqual(prop, {'c': 2})

    def test_prune_nested(self):
        prop = Dict(TEST_DICT)
        prop.b.c.d
        prop.d
        prop.prune()
        self.assertDictEqual(prop, TEST_DICT)

    def test_prune_empty_list(self):
        prop = Dict(TEST_DICT)
        prop.b.c = []
        prop.prune()
        self.assertDictEqual(prop, TEST_DICT)

    def test_prune_shared_key(self):
        prop = Dict(TEST_DICT)
        prop.a.b.d
        prop.prune()
        self.assertDictEqual(prop, TEST_DICT)

    def test_prune_dont_remove_zero(self):
        prop = Dict()
        prop.a = 0
        prop.b.c
        prop.prune()
        self.assertDictEqual(prop, {'a': 0})

    def test_prune_with_list(self):
        prop = Dict()
        prop.a = [Dict(), Dict(), Dict()]
        prop.a[0].b.c = 2
        prop.prune()
        self.assertDictEqual(prop, {'a': [{'b': {'c': 2}}]})

    def test_prune_list(self):
        l = [Dict(), Dict(), Dict()]
        l[0].a.b = 2
        l1 = Dict._prune_list(l)
        self.assertSequenceEqual(l1, [{'a': {'b': 2}}])

    def test_prune_not_new_list(self):
        prop = Dict()
        prop.a.b = []
        prop.b = 2
        prop.prune()
        self.assertDictEqual(prop, {'b': 2})

    def test_list_reduce(self):
        prop = Dict()
        prop.a = [Dict(), 1, 2]
        prop.a[0].b.c
        prop.prune()
        self.assertDictEqual(prop, {'a': [1, 2]})

    def test_list_reduce_nested_list(self):
        prop = Dict()
        prop.a = [Dict(), [[]], [1,2,3]]
        prop.prune()
        self.assertDictEqual(prop, {'a': [[1,2,3]]})
