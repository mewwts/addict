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

    def test_init_with_dict(self):
        self.assertDictEqual(TEST_DICT, Dict(TEST_DICT))

    def test_init_with_kws(self):
        prop = Dict(a=2, b={'a': 2}, c=[{'a':2}])
        self.assertDictEqual(prop, {'a': 2, 'b': {'a': 2}, 'c': [{'a': 2}]})

    def test_init_with_tuples(self):
        prop = Dict((0, 1), (1, 2), (2, 3))
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_list(self):
        prop = Dict([(0, 1), (1, 2), (2, 3)])
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_generator(self):
        prop = Dict(((i, i+1) for i in range(3)))
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_tuples_and_empty_list(self):
        prop = Dict((0, 1), [], (2, 3))
        self.assertDictEqual(prop, {0: 1, 2: 3})

    def test_init_raises(self):
        def init():
            Dict(5)
        def init2():
            Dict('a')
        self.assertRaises(TypeError, init)
        self.assertRaises(TypeError, init2)

    def test_init_with_empty_stuff(self):
        a = Dict({})
        b = Dict([])
        self.assertDictEqual(a, {})
        self.assertDictEqual(b, {})

    def test_init_with_list_of_dicts(self):
        a = Dict({'a': [{'b': 2}]})
        self.assertIsInstance(a.a[0], Dict)
        self.assertEqual(a.a[0].b, 2)

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

    def test_prune_with_tuple(self):
        prop = Dict()
        prop.a = (Dict(), Dict(), Dict())
        prop.a[0].b.c = 2
        prop.prune()
        self.assertDictEqual(prop, {'a': ({'b': {'c': 2}}, )})

    def test_prune_list(self):
        l = [Dict(), Dict(), Dict()]
        l[0].a.b = 2
        l1 = Dict._prune_iter(l)
        self.assertSequenceEqual(l1, [{'a': {'b': 2}}])

    def test_prune_tuple(self):
        l = (Dict(), Dict(), Dict())
        l[0].a.b = 2
        l1 = Dict._prune_iter(l)
        self.assertSequenceEqual(l1, [{'a': {'b': 2}}])

    def test_prune_not_new_list(self):
        prop = Dict()
        prop.a.b = []
        prop.b = 2
        prop.prune()
        self.assertDictEqual(prop, {'b': 2})

    def test_iter_reduce(self):
        prop = Dict()
        prop.a = [Dict(), 1, 2]
        prop.a[0].b.c
        prop.prune()
        self.assertDictEqual(prop, {'a': [1, 2]})

    def test_iter_reduce(self):
        prop = Dict()
        prop.a = (Dict(), 1, 2)
        prop.a[0].b.c
        prop.prune()
        self.assertDictEqual(prop, {'a': (1, 2)})

    def test_prune_nested_list(self):
        prop = Dict()
        prop.a = [Dict(), [[]], [1,2,3]]
        prop.prune()
        self.assertDictEqual(prop, {'a': [[1,2,3]]})

    def test_complex_nested_structure(self):
        prop = Dict()
        prop.a = [(Dict(), 2), [[]], [1, (2, 3), 0]]
        prop.prune(prune_zero=True)
        self.assertDictEqual(prop, {'a': [(2,), [1, (2, 3)]]})

    def test_tuple_key(self):
        prop = Dict()
        prop[(1, 2)] = 2
        self.assertDictEqual(prop, {(1, 2): 2})
        self.assertEqual(prop[(1, 2)], 2)

    def test_repr_html(self):
        prop = Dict()
        prop.a.b.c = TEST_VAL
        self.assertEqual(prop._repr_html_(), TEST_DICT_STR)

    def test_set_prop_invalid(self):
        prop = Dict()

        def set_keys():
            prop.keys = 2

        def set_items():
            prop.items = 3

        self.assertRaises(AttributeError, set_keys)
        self.assertRaises(AttributeError, set_items)
        self.assertDictEqual(prop, {})

    def test_dir(self):
        prop = Dict({'a': 1})
        dir_prop = dir(prop)
        self.assertEqual(dir_prop, dir(Dict))
        self.assertTrue('__methods__' not in dir_prop)
        self.assertTrue('__members__' not in dir_prop)

    def test_dir_with_members(self):
        prop = Dict({'__members__': 1})
        dir(prop)
        self.assertTrue('__members__' in prop.keys())

    def test_prune_zero(self):
        prop = Dict({'a': 1, 'c': 0})
        prop.prune(prune_zero=True)
        self.assertDictEqual(prop, {'a': 1})

    def test_prune_zero_nested(self):
        prop = Dict({'a': 1, 'c': {'d': 0}})
        prop.prune(prune_zero=True)
        self.assertDictEqual(prop, {'a': 1})

    def test_prune_zero_in_tuple(self):
        prop = Dict({'a': 1, 'c': (1, 0)})
        prop.prune(prune_zero=True)
        self.assertDictEqual(prop, {'a': 1, 'c': (1, )})

    def test_prune_empty_list_nested(self):
        prop = Dict({'a': 1, 'c': {'d': []}})
        prop.prune()
        self.assertDictEqual(prop, {'a': 1})

    def test_not_prune_empty_list_nested(self):
        prop = Dict({'a': 1, 'c': ([], )})
        prop.prune(prune_empty_list=False)
        self.assertDictEqual(prop, {'a': 1, 'c': ([], )})

    def test_do_not_prune_empty_list_nested(self):
        prop = Dict({'a': 1, 'c': {'d': []}})
        prop.prune(prune_empty_list=False)
        self.assertDictEqual(prop, {'a': 1, 'c': {'d': []}})

    def test_to_dict(self):
        nested = {'a': [{'a': 0}, 2], 'b': {}, 'c': 2}
        prop = Dict(nested)
        regular = prop.to_dict()
        self.assertDictEqual(regular, prop)
        self.assertDictEqual(regular, nested)
        self.assertNotIsInstance(regular, Dict)
        def get_attr():
            regular.a = 2
        self.assertRaises(AttributeError, get_attr)
        def get_attr_deep():
            regular['a'][0].a = 1
        self.assertRaises(AttributeError, get_attr_deep)

    def test_to_dict_with_tuple(self):
        nested = {'a': ({'a': 0}, {2: 0})}
        prop = Dict(nested)
        regular = prop.to_dict()
        self.assertDictEqual(regular, prop)
        self.assertDictEqual(regular, nested)
        self.assertIsInstance(regular['a'], tuple)
        self.assertNotIsInstance(regular['a'][0], Dict)


"""
Allow for these test cases to be run from the command line
via `python test_addict.py`
"""
if __name__ == '__main__':
    all_tests = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=2).run(all_tests)
