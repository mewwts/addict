import json
import copy
import unittest
import pickle
from addict import Dict


# test whether unittests pass on child classes
class CHILD_CLASS(Dict):
    child_class_attribute = 'child class attribute'

    def child_instance_attribute(self):
        return 'child instance attribute'


TEST_VAL = [1, 2, 3]
TEST_DICT = {'a': {'b': {'c': TEST_VAL}}}


class AbstractTestsClass(object):
    dict_class = None

    def test_set_one_level_item(self):
        some_dict = {'a': TEST_VAL}
        prop = self.dict_class()
        prop['a'] = TEST_VAL
        self.assertDictEqual(prop, some_dict)

    def test_set_two_level_items(self):
        some_dict = {'a': {'b': TEST_VAL}}
        prop = self.dict_class()
        prop['a']['b'] = TEST_VAL
        self.assertDictEqual(prop, some_dict)

    def test_set_three_level_items(self):
        prop = self.dict_class()
        prop['a']['b']['c'] = TEST_VAL
        self.assertDictEqual(prop, TEST_DICT)

    def test_set_one_level_property(self):
        prop = self.dict_class()
        prop.a = TEST_VAL
        self.assertDictEqual(prop, {'a': TEST_VAL})

    def test_set_two_level_properties(self):
        prop = self.dict_class()
        prop.a.b = TEST_VAL
        self.assertDictEqual(prop, {'a': {'b': TEST_VAL}})

    def test_set_three_level_properties(self):
        prop = self.dict_class()
        prop.a.b.c = TEST_VAL
        self.assertDictEqual(prop, TEST_DICT)

    def test_init_with_dict(self):
        self.assertDictEqual(TEST_DICT, Dict(TEST_DICT))

    def test_init_with_kws(self):
        prop = self.dict_class(a=2, b={'a': 2}, c=[{'a': 2}])
        self.assertDictEqual(prop, {'a': 2, 'b': {'a': 2}, 'c': [{'a': 2}]})

    def test_init_with_tuples(self):
        prop = self.dict_class((0, 1), (1, 2), (2, 3))
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_list(self):
        prop = self.dict_class([(0, 1), (1, 2), (2, 3)])
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_generator(self):
        prop = self.dict_class(((i, i + 1) for i in range(3)))
        self.assertDictEqual(prop, {0: 1, 1: 2, 2: 3})

    def test_init_with_tuples_and_empty_list(self):
        prop = self.dict_class((0, 1), [], (2, 3))
        self.assertDictEqual(prop, {0: 1, 2: 3})

    def test_init_raises(self):
        def init():
            self.dict_class(5)

        def init2():
            Dict('a')
        self.assertRaises(TypeError, init)
        self.assertRaises(ValueError, init2)

    def test_init_with_empty_stuff(self):
        a = self.dict_class({})
        b = self.dict_class([])
        self.assertDictEqual(a, {})
        self.assertDictEqual(b, {})

    def test_init_with_list_of_dicts(self):
        a = self.dict_class({'a': [{'b': 2}]})
        self.assertIsInstance(a.a[0], self.dict_class)
        self.assertEqual(a.a[0].b, 2)

    def test_init_with_kwargs(self):
        a = self.dict_class(a='b', c=dict(d='e', f=dict(g='h')))

        self.assertEqual(a.a, 'b')
        self.assertIsInstance(a.c, self.dict_class)

        self.assertEqual(a.c.f.g, 'h')
        self.assertIsInstance(a.c.f, self.dict_class)

    def test_getitem(self):
        prop = self.dict_class(TEST_DICT)
        self.assertEqual(prop['a']['b']['c'], TEST_VAL)

    def test_empty_getitem(self):
        prop = self.dict_class()
        prop.a.b.c
        self.assertEqual(prop, {})

    def test_getattr(self):
        prop = self.dict_class(TEST_DICT)
        self.assertEqual(prop.a.b.c, TEST_VAL)

    def test_isinstance(self):
        self.assertTrue(isinstance(self.dict_class(), dict))

    def test_str(self):
        prop = self.dict_class(TEST_DICT)
        self.assertEqual(str(prop), str(TEST_DICT))

    def test_json(self):
        some_dict = TEST_DICT
        some_json = json.dumps(some_dict)
        prop = self.dict_class()
        prop.a.b.c = TEST_VAL
        prop_json = json.dumps(prop)
        self.assertEqual(some_json, prop_json)

    def test_delitem(self):
        prop = self.dict_class({'a': 2})
        del prop['a']
        self.assertDictEqual(prop, {})

    def test_delitem_nested(self):
        prop = self.dict_class(TEST_DICT)
        del prop['a']['b']['c']
        self.assertDictEqual(prop, {'a': {'b': {}}})

    def test_delattr(self):
        prop = self.dict_class({'a': 2})
        del prop.a
        self.assertDictEqual(prop, {})

    def test_delattr_nested(self):
        prop = self.dict_class(TEST_DICT)
        del prop.a.b.c
        self.assertDictEqual(prop, {'a': {'b': {}}})

    def test_delitem_delattr(self):
        prop = self.dict_class(TEST_DICT)
        del prop.a['b']
        self.assertDictEqual(prop, {'a': {}})

    def test_tuple_key(self):
        prop = self.dict_class()
        prop[(1, 2)] = 2
        self.assertDictEqual(prop, {(1, 2): 2})
        self.assertEqual(prop[(1, 2)], 2)

    def test_set_prop_invalid(self):
        prop = self.dict_class()

        def set_keys():
            prop.keys = 2

        def set_items():
            prop.items = 3

        self.assertRaises(AttributeError, set_keys)
        self.assertRaises(AttributeError, set_items)
        self.assertDictEqual(prop, {})

    def test_dir(self):
        key = 'a'
        prop = self.dict_class({key: 1})
        dir_prop = dir(prop)

        dir_dict = dir(self.dict_class)
        for d in dir_dict:
            self.assertTrue(d in dir_prop, d)

        self.assertTrue('__methods__' not in dir_prop)
        self.assertTrue('__members__' not in dir_prop)

    def test_dir_with_members(self):
        prop = self.dict_class({'__members__': 1})
        dir(prop)
        self.assertTrue('__members__' in prop.keys())

    def test_to_dict(self):
        nested = {'a': [{'a': 0}, 2], 'b': {}, 'c': 2}
        prop = self.dict_class(nested)
        regular = prop.to_dict()
        self.assertDictEqual(regular, prop)
        self.assertDictEqual(regular, nested)
        self.assertNotIsInstance(regular, self.dict_class)

        def get_attr():
            regular.a = 2
        self.assertRaises(AttributeError, get_attr)

        def get_attr_deep():
            regular['a'][0].a = 1
        self.assertRaises(AttributeError, get_attr_deep)

    def test_to_dict_with_tuple(self):
        nested = {'a': ({'a': 0}, {2: 0})}
        prop = self.dict_class(nested)
        regular = prop.to_dict()
        self.assertDictEqual(regular, prop)
        self.assertDictEqual(regular, nested)
        self.assertIsInstance(regular['a'], tuple)
        self.assertNotIsInstance(regular['a'][0], self.dict_class)

    def test_update(self):
        old = self.dict_class()
        old.child.a = 'a'
        old.child.b = 'b'
        old.foo = 'c'

        new = self.dict_class()
        new.child.b = 'b2'
        new.child.c = 'c'
        new.foo.bar = True

        old.update(new)

        reference = {'foo': {'bar': True},
                     'child': {'a': 'a', 'c': 'c', 'b': 'b2'}}

        self.assertDictEqual(old, reference)

    def test_update_with_lists(self):
        org = self.dict_class()
        org.a = [1, 2, {'a': 'superman'}]
        someother = self.dict_class()
        someother.b = [{'b': 123}]
        org.update(someother)

        correct = {'a': [1, 2, {'a': 'superman'}],
                   'b': [{'b': 123}]}

        org.update(someother)
        self.assertDictEqual(org, correct)
        self.assertIsInstance(org.b[0], dict)

    def test_update_with_kws(self):
        org = self.dict_class(one=1, two=2)
        someother = self.dict_class(one=3)
        someother.update(one=1, two=2)
        self.assertDictEqual(org, someother)

    def test_update_with_args_and_kwargs(self):
        expected = {'a': 1, 'b': 2}
        org = self.dict_class()
        org.update({'a': 3, 'b': 2}, a=1)
        self.assertDictEqual(org, expected)

    def test_update_with_multiple_args(self):
        def update():
            org.update({'a': 2}, {'a': 1})
        org = self.dict_class()
        self.assertRaises(TypeError, update)
        
    def test_ior_operator(self):
        old = self.dict_class()
        old.child.a = 'a'
        old.child.b = 'b'
        old.foo = 'c'

        new = self.dict_class()
        new.child.b = 'b2'
        new.child.c = 'c'
        new.foo.bar = True

        old |= new

        reference = {'foo': {'bar': True},
                     'child': {'a': 'a', 'c': 'c', 'b': 'b2'}}

        self.assertDictEqual(old, reference)

    def test_ior_operator_with_lists(self):
        org = self.dict_class()
        org.a = [1, 2, {'a': 'superman'}]
        someother = self.dict_class()
        someother.b = [{'b': 123}]
        org |= someother

        correct = {'a': [1, 2, {'a': 'superman'}],
                   'b': [{'b': 123}]}

        org |= someother
        self.assertDictEqual(org, correct)
        self.assertIsInstance(org.b[0], dict)

    def test_ior_operator_with_dict(self):
        org = self.dict_class(one=1, two=2)
        someother = self.dict_class(one=3)
        someother |= dict(one=1, two=2)
        self.assertDictEqual(org, someother)

    def test_or_operator(self):
        old = self.dict_class()
        old.child.a = 'a'
        old.child.b = 'b'
        old.foo = 'c'

        new = self.dict_class()
        new.child.b = 'b2'
        new.child.c = 'c'
        new.foo.bar = True

        old = old | new

        reference = {'foo': {'bar': True},
                     'child': {'a': 'a', 'c': 'c', 'b': 'b2'}}

        self.assertDictEqual(old, reference)

    def test_or_operator_with_lists(self):
        org = self.dict_class()
        org.a = [1, 2, {'a': 'superman'}]
        someother = self.dict_class()
        someother.b = [{'b': 123}]
        org = org | someother

        correct = {'a': [1, 2, {'a': 'superman'}],
                   'b': [{'b': 123}]}

        org = org | someother
        self.assertDictEqual(org, correct)
        self.assertIsInstance(org.b[0], dict)
    
    def test_ror_operator(self):
        org = dict()
        org['a'] = [1, 2, {'a': 'superman'}]
        someother = self.dict_class()
        someother.b = [{'b': 123}]
        org = org | someother

        correct = {'a': [1, 2, {'a': 'superman'}],
                   'b': [{'b': 123}]}

        org = org | someother
        self.assertDictEqual(org, correct)
        self.assertIsInstance(org, Dict)
        self.assertIsInstance(org.b[0], dict)
  
    def test_or_operator_type_error(self):
        old = self.dict_class()
        with self.assertRaises(TypeError):
            old | 'test'

    def test_ror_operator_type_error(self):
        old = self.dict_class()
        with self.assertRaises(TypeError):
            'test' | old

    def test_hook_in_constructor(self):
        a_dict = self.dict_class(TEST_DICT)
        self.assertIsInstance(a_dict['a'], self.dict_class)

    def test_copy(self):
        class MyMutableObject(object):

            def __init__(self):
                self.attribute = None

        foo = MyMutableObject()
        foo.attribute = True

        a = self.dict_class()
        a.child.immutable = 42
        a.child.mutable = foo

        b = a.copy()

        # immutable object should not change
        b.child.immutable = 21
        self.assertEqual(a.child.immutable, 21)

        # mutable object should change
        b.child.mutable.attribute = False
        self.assertEqual(a.child.mutable.attribute, b.child.mutable.attribute)

        # changing child of b should not affect a
        b.child = "new stuff"
        self.assertTrue(isinstance(a.child, self.dict_class))

    def test_deepcopy(self):
        class MyMutableObject(object):
            def __init__(self):
                self.attribute = None

        foo = MyMutableObject()
        foo.attribute = True

        a = self.dict_class()
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
        self.assertTrue(isinstance(a.child, self.dict_class))

    def test_deepcopy2(self):
        class MyMutableObject(object):
            def __init__(self):
                self.attribute = None

        foo = MyMutableObject()
        foo.attribute = True

        a = self.dict_class()
        a.child.immutable = 42
        a.child.mutable = foo

        b = a.deepcopy()

        # immutable object should not change
        b.child.immutable = 21
        self.assertEqual(a.child.immutable, 42)

        # mutable object should not change
        b.child.mutable.attribute = False
        self.assertTrue(a.child.mutable.attribute)

        # changing child of b should not affect a
        b.child = "new stuff"
        self.assertTrue(isinstance(a.child, self.dict_class))

    def test_pickle(self):
        a = self.dict_class(TEST_DICT)
        self.assertEqual(a, pickle.loads(pickle.dumps(a)))

    def test_add_on_empty_dict(self):
        d = self.dict_class()
        d.x.y += 1

        self.assertEqual(d.x.y, 1)

    def test_add_on_non_empty_dict(self):
        d = self.dict_class()
        d.x.y = 'defined'

        with self.assertRaises(TypeError):
            d.x += 1

    def test_add_on_non_empty_value(self):
        d = self.dict_class()
        d.x.y = 1
        d.x.y += 1

        self.assertEqual(d.x.y, 2)

    def test_add_on_unsupported_type(self):
        d = self.dict_class()
        d.x.y = 'str'

        with self.assertRaises(TypeError):
            d.x.y += 1

    def test_init_from_zip(self):
        keys = ['a']
        values = [42]
        items = zip(keys, values)
        d = self.dict_class(items)
        self.assertEqual(d.a, 42)

    def test_setdefault_simple(self):
        d = self.dict_class()
        d.setdefault('a', 2)
        self.assertEqual(d.a, 2)
        d.setdefault('a', 3)
        self.assertEqual(d.a, 2)
        d.setdefault('c', []).append(2)
        self.assertEqual(d.c, [2])

    def test_setdefault_nested(self):
        d = self.dict_class()
        d.one.setdefault('two', [])
        self.assertEqual(d.one.two, [])
        d.one.setdefault('three', []).append(3)
        self.assertEqual(d.one.three, [3])

    def test_parent_key_item(self):
        a = self.dict_class()
        try:
            a['keys']['x'] = 1
        except AttributeError as e:
            self.fail(e)
        try:
            a[1].x = 3
        except Exception as e:
            self.fail(e)
        self.assertEqual(a, {'keys': {'x': 1}, 1: {'x': 3}})

    def test_parent_key_prop(self):
        a = self.dict_class()
        try:
            a.y.x = 1
        except AttributeError as e:
            self.fail(e)
        self.assertEqual(a, {'y': {'x': 1}})

    def test_top_freeze_against_top_key(self):
        "Test that d.freeze() produces KeyError on d.missing."
        d = self.dict_class()
        self.assertEqual(d.missing, {})
        d.freeze()
        with self.assertRaises(KeyError):
            d.missing
        d.unfreeze()
        self.assertEqual(d.missing, {})

    def test_top_freeze_against_nested_key(self):
        "Test that d.freeze() produces KeyError on d.inner.missing."
        d = self.dict_class()
        d.inner.present = TEST_VAL
        self.assertIn("inner", d)
        self.assertEqual(d.inner.missing, {})
        d.freeze()
        with self.assertRaises(KeyError):
            d.inner.missing
        with self.assertRaises(KeyError):
            d.missing
        d.unfreeze()
        self.assertEqual(d.inner.missing, {})
        self.assertEqual(d.missing, {})

    def test_nested_freeze_against_top_level(self):
        "Test that d.inner.freeze() leaves top-level `d` unfrozen."
        d = self.dict_class()
        d.inner.present = TEST_VAL
        self.assertEqual(d.inner.present, TEST_VAL)
        self.assertEqual(d.inner.missing, {})
        self.assertEqual(d.missing, {})
        d.inner.freeze()
        with self.assertRaises(KeyError):
            d.inner.missing             # d.inner is frozen
        self.assertEqual(d.missing, {}) # but not `d` itself
        d.inner.unfreeze()
        self.assertEqual(d.inner.missing, {})

    def test_top_freeze_disallows_new_key_addition(self):
        "Test that d.freeze() disallows adding new keys in d."
        d = self.dict_class({"oldKey": None})
        d.freeze()
        d.oldKey = TEST_VAL         # Can set pre-existing key.
        self.assertEqual(d.oldKey, TEST_VAL)
        with self.assertRaises(KeyError):
            d.newKey = TEST_VAL     # But can't add a new key.
        self.assertNotIn("newKey", d)
        d.unfreeze()
        d.newKey = TEST_VAL
        self.assertEqual(d.newKey, TEST_VAL)

class DictTests(unittest.TestCase, AbstractTestsClass):
    dict_class = Dict


class ChildDictTests(unittest.TestCase, AbstractTestsClass):
    dict_class = CHILD_CLASS

"""
Allow for these test cases to be run from the command line
via `python test_addict.py`
"""
if __name__ == '__main__':
    test_classes = (DictTests, ChildDictTests)
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    for class_ in test_classes:
        loaded_tests = loader.loadTestsFromTestCase(class_)
        runner.run(loaded_tests)
