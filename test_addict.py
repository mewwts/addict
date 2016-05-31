import json
import copy
import unittest
from addict import Dict, OrderedDict

TEST_VAL = [1, 2, 3]
TEST_DICT = {'a': {'b': {'c': TEST_VAL}}}
TEST_DICT_STR = str(TEST_DICT)


class BaseTests(unittest.TestCase):

    def test_set_one_level_item(self):
        some_dict = {'a': TEST_VAL}
        prop = self.DictClass()
        prop['a'] = TEST_VAL
        self.assertDictEqual(prop, some_dict)

    def test_set_two_level_items(self):
        some_dict = {'a': {'b': TEST_VAL}}
        prop = self.DictClass()
        prop['a']['b'] = TEST_VAL
        self.assertDictEqual(prop, some_dict)

    def test_set_three_level_items(self):
        prop = self.DictClass()
        prop['a']['b']['c'] = TEST_VAL
        self.assertDictEqual(prop, TEST_DICT)

    def test_set_one_level_property(self):
        prop = self.DictClass()
        prop.a = TEST_VAL
        self.assertDictEqual(prop, {'a': TEST_VAL})

    def test_set_two_level_properties(self):
        prop = self.DictClass()
        prop.a.b = TEST_VAL
        self.assertDictEqual(prop, {'a': {'b': TEST_VAL}})

    def test_set_three_level_properties(self):
        prop = self.DictClass()
        prop.a.b.c = TEST_VAL
        self.assertDictEqual(prop, TEST_DICT)

    def test_init_with_dict(self):
        self.assertDictEqual(TEST_DICT, self.DictClass(TEST_DICT))

    def test_init_with_kws(self):
        prop = self.DictClass(a=2, b={'a': 2}, c=[{'a': 2}])
        self.assertDictEqual(prop, {'a': 2, 'b': {'a': 2}, 'c': [{'a': 2}]})

    def test_init_with_tuples(self):
        prop = self.DictClass((0, 1), (1, 2), (2, 3))
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_list(self):
        prop = self.DictClass([(0, 1), (1, 2), (2, 3)])
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_generator(self):
        prop = self.DictClass(((i, i + 1) for i in range(3)))
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_tuples_and_empty_list(self):
        prop = self.DictClass((0, 1), [], (2, 3))
        self.assertDictEqual(prop, {0: 1, 2: 3})

    def test_init_raises(self):
        def init():
            self.DictClass(5)

        def init2():
            self.DictClass('a')
        self.assertRaises(TypeError, init)
        self.assertRaises(TypeError, init2)

    def test_init_with_empty_stuff(self):
        a = self.DictClass({})
        b = self.DictClass([])
        self.assertDictEqual(a, {})
        self.assertDictEqual(b, {})

    def test_init_with_list_of_dicts(self):
        a = self.DictClass({'a': [{'b': 2}]})
        self.assertIsInstance(a.a[0], self.DictClass)
        self.assertEqual(a.a[0].b, 2)

    def test_getitem(self):
        prop = self.DictClass(TEST_DICT)
        self.assertEqual(prop['a']['b']['c'], TEST_VAL)

    def test_getattr(self):
        prop = self.DictClass(TEST_DICT)
        self.assertEqual(prop.a.b.c, TEST_VAL)

    def test_isinstance(self):
        self.assertTrue(isinstance(self.DictClass(), dict))

    def test_str(self):
        prop = self.DictClass(TEST_DICT)
        self.assertEqual(str(prop), str(TEST_DICT))

    def test_json(self):
        some_dict = TEST_DICT
        some_json = json.dumps(some_dict)
        prop = self.DictClass()
        prop.a.b.c = TEST_VAL
        prop_json = json.dumps(prop)
        self.assertEqual(some_json, prop_json)

    def test_delitem(self):
        prop = self.DictClass({'a': 2})
        del prop['a']
        self.assertDictEqual(prop, {})

    def test_delitem_nested(self):
        prop = self.DictClass(TEST_DICT)
        del prop['a']['b']['c']
        self.assertDictEqual(prop, {'a': {'b': {}}})

    def test_delattr(self):
        prop = self.DictClass({'a': 2})
        del prop.a
        self.assertDictEqual(prop, {})

    def test_delattr_nested(self):
        prop = self.DictClass(TEST_DICT)
        del prop.a.b.c
        self.assertDictEqual(prop, {'a': {'b': {}}})

    def test_delitem_delattr(self):
        prop = self.DictClass(TEST_DICT)
        del prop.a['b']
        self.assertDictEqual(prop, {'a': {}})

    def test_prune(self):
        prop = self.DictClass()
        prop.a.b.c.d
        prop.b
        prop.c = 2
        prop.prune()
        self.assertDictEqual(prop, {'c': 2})

    def test_prune_nested(self):
        prop = self.DictClass(TEST_DICT)
        prop.b.c.d
        prop.d
        prop.prune()
        self.assertDictEqual(prop, TEST_DICT)

    def test_prune_empty_list(self):
        prop = self.DictClass(TEST_DICT)
        prop.b.c = []
        prop.prune()
        self.assertDictEqual(prop, TEST_DICT)

    def test_prune_shared_key(self):
        prop = self.DictClass(TEST_DICT)
        prop.a.b.d
        prop.prune()
        self.assertDictEqual(prop, TEST_DICT)

    def test_prune_dont_remove_zero(self):
        prop = self.DictClass()
        prop.a = 0
        prop.b.c
        prop.prune()
        self.assertDictEqual(prop, {'a': 0})

    def test_prune_with_list(self):
        prop = self.DictClass()
        prop.a = [self.DictClass(), self.DictClass(), self.DictClass()]
        prop.a[0].b.c = 2
        prop.prune()
        self.assertDictEqual(prop, {'a': [{'b': {'c': 2}}]})

    def test_prune_with_tuple(self):
        prop = self.DictClass()
        prop.a = (self.DictClass(), self.DictClass(), self.DictClass())
        prop.a[0].b.c = 2
        prop.prune()
        self.assertDictEqual(prop, {'a': ({'b': {'c': 2}}, )})

    def test_prune_list(self):
        l = [self.DictClass(), self.DictClass(), self.DictClass()]
        l[0].a.b = 2
        l1 = self.DictClass._prune_iter(l)
        self.assertSequenceEqual(l1, [{'a': {'b': 2}}])

    def test_prune_tuple(self):
        l = (self.DictClass(), self.DictClass(), self.DictClass())
        l[0].a.b = 2
        l1 = self.DictClass._prune_iter(l)
        self.assertSequenceEqual(l1, [{'a': {'b': 2}}])

    def test_prune_not_new_list(self):
        prop = self.DictClass()
        prop.a.b = []
        prop.b = 2
        prop.prune()
        self.assertDictEqual(prop, {'b': 2})

    def test_iter_reduce_with_list(self):
        prop = self.DictClass()
        prop.a = [self.DictClass(), 1, 2]
        prop.a[0].b.c
        prop.prune()
        self.assertDictEqual(prop, {'a': [1, 2]})

    def test_iter_reduce_with_tuple(self):
        prop = self.DictClass()
        prop.a = (self.DictClass(), 1, 2)
        prop.a[0].b.c
        prop.prune()
        self.assertDictEqual(prop, {'a': (1, 2)})

    def test_prune_nested_list(self):
        prop = self.DictClass()
        prop.a = [self.DictClass(), [[]], [1, 2, 3]]
        prop.prune()
        self.assertDictEqual(prop, {'a': [[1, 2, 3]]})

    def test_complex_nested_structure(self):
        prop = self.DictClass()
        prop.a = [(self.DictClass(), 2), [[]], [1, (2, 3), 0]]
        prop.prune(prune_zero=True)
        self.assertDictEqual(prop, {'a': [(2,), [1, (2, 3)]]})

    def test_tuple_key(self):
        prop = self.DictClass()
        prop[(1, 2)] = 2
        self.assertDictEqual(prop, {(1, 2): 2})
        self.assertEqual(prop[(1, 2)], 2)

    def test_repr_html(self):
        prop = self.DictClass()
        prop.a.b.c = TEST_VAL
        self.assertEqual(prop._repr_html_(), TEST_DICT_STR)

    def test_set_prop_invalid(self):
        prop = self.DictClass()

        def set_keys():
            prop.keys = 2

        def set_items():
            prop.items = 3

        self.assertRaises(AttributeError, set_keys)
        self.assertRaises(AttributeError, set_items)
        self.assertDictEqual(prop, {})

    def test_dir(self):
        key = 'a'
        prop = self.DictClass({key: 1})
        dir_prop = dir(prop)

        dir_dict = dir(self.DictClass)
        for d in dir_dict:
            self.assertTrue(d in dir_prop, d)

        self.assertTrue(key in dir_prop)

        self.assertTrue('__methods__' not in dir_prop)
        self.assertTrue('__members__' not in dir_prop)

    def test_dir_with_members(self):
        prop = self.DictClass({'__members__': 1})
        dir(prop)
        self.assertTrue('__members__' in prop.keys())

    def test_prune_zero(self):
        prop = self.DictClass({'a': 1, 'c': 0})
        prop.prune(prune_zero=True)
        self.assertDictEqual(prop, {'a': 1})

    def test_prune_zero_nested(self):
        prop = self.DictClass({'a': 1, 'c': {'d': 0}})
        prop.prune(prune_zero=True)
        self.assertDictEqual(prop, {'a': 1})

    def test_prune_zero_in_tuple(self):
        prop = self.DictClass({'a': 1, 'c': (1, 0)})
        prop.prune(prune_zero=True)
        self.assertDictEqual(prop, {'a': 1, 'c': (1, )})

    def test_prune_empty_list_nested(self):
        prop = self.DictClass({'a': 1, 'c': {'d': []}})
        prop.prune()
        self.assertDictEqual(prop, {'a': 1})

    def test_not_prune_empty_list_nested(self):
        prop = self.DictClass({'a': 1, 'c': ([], )})
        prop.prune(prune_empty_list=False)
        self.assertDictEqual(prop, {'a': 1, 'c': ([], )})

    def test_do_not_prune_empty_list_nested(self):
        prop = self.DictClass({'a': 1, 'c': {'d': []}})
        prop.prune(prune_empty_list=False)
        self.assertDictEqual(prop, {'a': 1, 'c': {'d': []}})

    def test_to_dict(self):
        nested = {'a': [{'a': 0}, 2], 'b': {}, 'c': 2}
        prop = self.DictClass(nested)
        regular = prop.to_dict()
        self.assertDictEqual(regular, prop)
        self.assertDictEqual(regular, nested)
        self.assertNotIsInstance(regular, self.DictClass)

        def get_attr():
            regular.a = 2
        self.assertRaises(AttributeError, get_attr)

        def get_attr_deep():
            regular['a'][0].a = 1
        self.assertRaises(AttributeError, get_attr_deep)

    def test_to_dict_with_tuple(self):
        nested = {'a': ({'a': 0}, {2: 0})}
        prop = self.DictClass(nested)
        regular = prop.to_dict()
        self.assertDictEqual(regular, prop)
        self.assertDictEqual(regular, nested)
        self.assertIsInstance(regular['a'], tuple)
        self.assertNotIsInstance(regular['a'][0], self.DictClass)

    def test_update(self):
        old = self.DictClass()
        old.child.a = 'old a'
        old.child.b = 'old b'
        old.foo = 'no dict'

        new = self.DictClass()
        new.child.b = 'new b'
        new.child.c = 'new c'
        new.foo.now_my_papa_is_a_dict = True

        old.update(new)

        reference = {'foo': {'now_my_papa_is_a_dict': True},
                     'child': {'a': 'old a', 'c': 'new c', 'b': 'new b'}}

        self.assertDictEqual(old, reference)

    def test_update_with_lists(self):
        org = self.DictClass()
        org.a = [1, 2, {'a': 'superman'}]
        someother = self.DictClass()
        someother.b = [{'b': 123}]
        org.update(someother)

        correct = {'a': [1, 2, {'a': 'superman'}],
                   'b': [{'b': 123}]}

        org.update(someother)
        self.assertDictEqual(org, correct)
        self.assertIsInstance(org.b[0], self.DictClass)

    def test_copy(self):
        class MyMutableObject(object):

            def __init__(self):
                self.attribute = None

        foo = MyMutableObject()
        foo.attribute = True

        a = self.DictClass()
        a.child.immutable = 42
        a.child.mutable = foo

        b = a.copy()

        # immutable object should not change
        b.child.immutable = 21
        self.assertEqual(a.child.immutable, 42)

        # mutable object should change
        b.child.mutable.attribute = False
        self.assertEqual(a.child.mutable.attribute, b.child.mutable.attribute)

        # changing child of b should not affect a
        b.child = "new stuff"
        self.assertTrue(isinstance(a.child, self.DictClass))

    def test_deepcopy(self):
        class MyMutableObject(object):
            def __init__(self):
                self.attribute = None

        foo = MyMutableObject()
        foo.attribute = True

        a = self.DictClass()
        a.child.immutable = 42
        a.child.mutable = foo

        b = copy.deepcopy(a)

        # immutable object should not change
        b.child.immutable = 21
        self.assertEqual(a.child.immutable, 42)

        # mutable object should not change
        b.child.mutable.attribute = False
        self.assertTrue(a.child.mutable.attribute)

        # changing child of b should not affect a
        b.child = "new stuff"
        self.assertTrue(isinstance(a.child, self.DictClass))


class DictTests(BaseTests):
    def __init__(self, *args, **kwargs):
        self.DictClass = Dict
        super(DictTests, self).__init__(*args, **kwargs)


class OrderedDictTests(BaseTests):
    def __init__(self, *args, **kwargs):
        self.DictClass = OrderedDict
        super(OrderedDictTests, self).__init__(*args, **kwargs)


"""
Allow for these test cases to be run from the command line
via `python test_addict.py`
"""
if __name__ == '__main__':
    dict_tests = unittest.TestLoader().loadTestsFromTestCase(DictTests)
    orderedDict_tests = unittest.TestLoader().loadTestsFromTestCase(
        OrderedDictTests)

    unittest.TextTestRunner(verbosity=2).run(dict_tests)
    unittest.TextTestRunner(verbosity=2).run(orderedDict_tests)
