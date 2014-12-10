import json
import unittest
from bigdict import Dict

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

