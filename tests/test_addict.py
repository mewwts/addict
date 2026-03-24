from __future__ import annotations

import copy
import json
import pickle

import pytest

from addict import Dict

TEST_VAL = [1, 2, 3]
TEST_DICT = {"a": {"b": {"c": TEST_VAL}}}


class ChildDict(Dict):
    child_class_attribute = "child class attribute"

    def child_instance_attribute(self) -> str:
        return "child instance attribute"


@pytest.fixture(params=[Dict, ChildDict], ids=["Dict", "ChildDict"])
def dict_class(request: pytest.FixtureRequest) -> type[Dict]:
    return request.param


class MyMutableObject:
    def __init__(self) -> None:
        self.attribute: bool | None = None


# --- Basic set/get ---


def test_set_one_level_item(dict_class: type[Dict]) -> None:
    prop = dict_class()
    prop["a"] = TEST_VAL
    assert prop == {"a": TEST_VAL}


def test_set_two_level_items(dict_class: type[Dict]) -> None:
    prop = dict_class()
    prop["a"]["b"] = TEST_VAL
    assert prop == {"a": {"b": TEST_VAL}}


def test_set_three_level_items(dict_class: type[Dict]) -> None:
    prop = dict_class()
    prop["a"]["b"]["c"] = TEST_VAL
    assert prop == TEST_DICT


def test_set_one_level_property(dict_class: type[Dict]) -> None:
    prop = dict_class()
    prop.a = TEST_VAL
    assert prop == {"a": TEST_VAL}


def test_set_two_level_properties(dict_class: type[Dict]) -> None:
    prop = dict_class()
    prop.a.b = TEST_VAL
    assert prop == {"a": {"b": TEST_VAL}}


def test_set_three_level_properties(dict_class: type[Dict]) -> None:
    prop = dict_class()
    prop.a.b.c = TEST_VAL
    assert prop == TEST_DICT


# --- Initialization ---


def test_init_with_dict(dict_class: type[Dict]) -> None:
    assert TEST_DICT == Dict(TEST_DICT)


def test_init_with_kws(dict_class: type[Dict]) -> None:
    prop = dict_class(a=2, b={"a": 2}, c=[{"a": 2}])
    assert prop == {"a": 2, "b": {"a": 2}, "c": [{"a": 2}]}


def test_init_with_tuples(dict_class: type[Dict]) -> None:
    prop = dict_class((0, 1), (1, 2), (2, 3))
    assert prop == {0: 1, 1: 2, 2: 3}


def test_init_with_list(dict_class: type[Dict]) -> None:
    prop = dict_class([(0, 1), (1, 2), (2, 3)])
    assert prop == {0: 1, 1: 2, 2: 3}


def test_init_with_generator(dict_class: type[Dict]) -> None:
    prop = dict_class((i, i + 1) for i in range(3))
    assert prop == {0: 1, 1: 2, 2: 3}


def test_init_with_tuples_and_empty_list(dict_class: type[Dict]) -> None:
    prop = dict_class((0, 1), [], (2, 3))
    assert prop == {0: 1, 2: 3}


def test_init_raises(dict_class: type[Dict]) -> None:
    with pytest.raises(TypeError):
        dict_class(5)
    with pytest.raises(ValueError):
        Dict("a")


def test_init_with_empty_stuff(dict_class: type[Dict]) -> None:
    assert dict_class({}) == {}
    assert dict_class([]) == {}


def test_init_with_list_of_dicts(dict_class: type[Dict]) -> None:
    a = dict_class({"a": [{"b": 2}]})
    assert isinstance(a.a[0], dict_class)
    assert a.a[0].b == 2


def test_init_with_kwargs(dict_class: type[Dict]) -> None:
    a = dict_class(a="b", c=dict(d="e", f=dict(g="h")))
    assert a.a == "b"
    assert isinstance(a.c, dict_class)
    assert a.c.f.g == "h"
    assert isinstance(a.c.f, dict_class)


# --- Item access ---


def test_getitem(dict_class: type[Dict]) -> None:
    prop = dict_class(TEST_DICT)
    assert prop["a"]["b"]["c"] == TEST_VAL


def test_empty_getitem(dict_class: type[Dict]) -> None:
    prop = dict_class()
    prop.a.b.c
    assert prop == {}


def test_getattr(dict_class: type[Dict]) -> None:
    prop = dict_class(TEST_DICT)
    assert prop.a.b.c == TEST_VAL


def test_isinstance(dict_class: type[Dict]) -> None:
    assert isinstance(dict_class(), dict)


def test_str(dict_class: type[Dict]) -> None:
    prop = dict_class(TEST_DICT)
    assert str(prop) == str(TEST_DICT)


def test_json(dict_class: type[Dict]) -> None:
    some_json = json.dumps(TEST_DICT)
    prop = dict_class()
    prop.a.b.c = TEST_VAL
    assert json.dumps(prop) == some_json


# --- Deletion ---


def test_delitem(dict_class: type[Dict]) -> None:
    prop = dict_class({"a": 2})
    del prop["a"]
    assert prop == {}


def test_delitem_nested(dict_class: type[Dict]) -> None:
    prop = dict_class(TEST_DICT)
    del prop["a"]["b"]["c"]
    assert prop == {"a": {"b": {}}}


def test_delattr(dict_class: type[Dict]) -> None:
    prop = dict_class({"a": 2})
    del prop.a
    assert prop == {}


def test_delattr_nested(dict_class: type[Dict]) -> None:
    prop = dict_class(TEST_DICT)
    del prop.a.b.c
    assert prop == {"a": {"b": {}}}


def test_delitem_delattr(dict_class: type[Dict]) -> None:
    prop = dict_class(TEST_DICT)
    del prop.a["b"]
    assert prop == {"a": {}}


# --- Special keys ---


def test_tuple_key(dict_class: type[Dict]) -> None:
    prop = dict_class()
    prop[(1, 2)] = 2
    assert prop == {(1, 2): 2}
    assert prop[(1, 2)] == 2


def test_set_prop_invalid(dict_class: type[Dict]) -> None:
    prop = dict_class()
    with pytest.raises(AttributeError):
        prop.keys = 2
    with pytest.raises(AttributeError):
        prop.items = 3
    assert prop == {}


def test_dir(dict_class: type[Dict]) -> None:
    prop = dict_class({"a": 1})
    dir_prop = dir(prop)
    for d in dir(dict_class):
        assert d in dir_prop
    assert "__methods__" not in dir_prop
    assert "__members__" not in dir_prop


def test_dir_with_members(dict_class: type[Dict]) -> None:
    prop = dict_class({"__members__": 1})
    dir(prop)
    assert "__members__" in prop.keys()


# --- to_dict ---


def test_to_dict(dict_class: type[Dict]) -> None:
    nested = {"a": [{"a": 0}, 2], "b": {}, "c": 2}
    prop = dict_class(nested)
    regular = prop.to_dict()
    assert regular == prop
    assert regular == nested
    assert not isinstance(regular, dict_class)
    with pytest.raises(AttributeError):
        regular.a = 2  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        regular["a"][0].a = 1  # type: ignore[attr-defined]


def test_to_dict_with_tuple(dict_class: type[Dict]) -> None:
    nested = {"a": ({"a": 0}, {2: 0})}
    prop = dict_class(nested)
    regular = prop.to_dict()
    assert regular == prop
    assert regular == nested
    assert isinstance(regular["a"], tuple)
    assert not isinstance(regular["a"][0], dict_class)


# --- Update ---


def test_update(dict_class: type[Dict]) -> None:
    old = dict_class()
    old.child.a = "a"
    old.child.b = "b"
    old.foo = "c"

    new = dict_class()
    new.child.b = "b2"
    new.child.c = "c"
    new.foo.bar = True

    old.update(new)
    assert old == {"foo": {"bar": True}, "child": {"a": "a", "c": "c", "b": "b2"}}


def test_update_with_lists(dict_class: type[Dict]) -> None:
    org = dict_class()
    org.a = [1, 2, {"a": "superman"}]
    someother = dict_class()
    someother.b = [{"b": 123}]
    org.update(someother)

    correct = {"a": [1, 2, {"a": "superman"}], "b": [{"b": 123}]}
    org.update(someother)
    assert org == correct
    assert isinstance(org.b[0], dict)


def test_update_with_kws(dict_class: type[Dict]) -> None:
    org = dict_class(one=1, two=2)
    someother = dict_class(one=3)
    someother.update(one=1, two=2)
    assert org == someother


def test_update_with_args_and_kwargs(dict_class: type[Dict]) -> None:
    org = dict_class()
    org.update({"a": 3, "b": 2}, a=1)
    assert org == {"a": 1, "b": 2}


def test_update_with_multiple_args(dict_class: type[Dict]) -> None:
    org = dict_class()
    with pytest.raises(TypeError):
        org.update({"a": 2}, {"a": 1})


# --- Merge operators ---


def test_ior_operator(dict_class: type[Dict]) -> None:
    old = dict_class()
    old.child.a = "a"
    old.child.b = "b"
    old.foo = "c"

    new = dict_class()
    new.child.b = "b2"
    new.child.c = "c"
    new.foo.bar = True

    old |= new
    assert old == {"foo": {"bar": True}, "child": {"a": "a", "c": "c", "b": "b2"}}


def test_ior_operator_with_lists(dict_class: type[Dict]) -> None:
    org = dict_class()
    org.a = [1, 2, {"a": "superman"}]
    someother = dict_class()
    someother.b = [{"b": 123}]
    org |= someother

    correct = {"a": [1, 2, {"a": "superman"}], "b": [{"b": 123}]}
    org |= someother
    assert org == correct
    assert isinstance(org.b[0], dict)


def test_ior_operator_with_dict(dict_class: type[Dict]) -> None:
    org = dict_class(one=1, two=2)
    someother = dict_class(one=3)
    someother |= dict(one=1, two=2)
    assert org == someother


def test_or_operator(dict_class: type[Dict]) -> None:
    old = dict_class()
    old.child.a = "a"
    old.child.b = "b"
    old.foo = "c"

    new = dict_class()
    new.child.b = "b2"
    new.child.c = "c"
    new.foo.bar = True

    old = old | new
    assert old == {"foo": {"bar": True}, "child": {"a": "a", "c": "c", "b": "b2"}}


def test_or_operator_with_lists(dict_class: type[Dict]) -> None:
    org = dict_class()
    org.a = [1, 2, {"a": "superman"}]
    someother = dict_class()
    someother.b = [{"b": 123}]
    org = org | someother

    correct = {"a": [1, 2, {"a": "superman"}], "b": [{"b": 123}]}
    org = org | someother
    assert org == correct
    assert isinstance(org.b[0], dict)


def test_ror_operator(dict_class: type[Dict]) -> None:
    org = {}
    org["a"] = [1, 2, {"a": "superman"}]
    someother = dict_class()
    someother.b = [{"b": 123}]
    org = org | someother

    correct = {"a": [1, 2, {"a": "superman"}], "b": [{"b": 123}]}
    org = org | someother
    assert org == correct
    assert isinstance(org, Dict)
    assert isinstance(org.b[0], dict)


def test_or_operator_type_error(dict_class: type[Dict]) -> None:
    old = dict_class()
    with pytest.raises(TypeError):
        old | "test"


def test_ror_operator_type_error(dict_class: type[Dict]) -> None:
    old = dict_class()
    with pytest.raises(TypeError):
        "test" | old


# --- Hook ---


def test_hook_in_constructor(dict_class: type[Dict]) -> None:
    a_dict = dict_class(TEST_DICT)
    assert isinstance(a_dict["a"], dict_class)


# --- Copy ---


def test_copy(dict_class: type[Dict]) -> None:
    foo = MyMutableObject()
    foo.attribute = True

    a = dict_class()
    a.child.immutable = 42
    a.child.mutable = foo

    b = a.copy()

    # immutable object should not change
    b.child.immutable = 21
    assert a.child.immutable == 21

    # mutable object should change
    b.child.mutable.attribute = False
    assert a.child.mutable.attribute == b.child.mutable.attribute

    # changing child of b should not affect a
    b.child = "new stuff"
    assert isinstance(a.child, dict_class)


def test_deepcopy(dict_class: type[Dict]) -> None:
    foo = MyMutableObject()
    foo.attribute = True

    a = dict_class()
    a.child.immutable = 42
    a.child.mutable = foo

    b = copy.deepcopy(a)

    # immutable object should not change
    b.child.immutable = 21
    assert a.child.immutable == 42

    # mutable object should not change
    b.child.mutable.attribute = False
    assert a.child.mutable.attribute is True

    # changing child of b should not affect a
    b.child = "new stuff"
    assert isinstance(a.child, dict_class)


def test_deepcopy_method(dict_class: type[Dict]) -> None:
    foo = MyMutableObject()
    foo.attribute = True

    a = dict_class()
    a.child.immutable = 42
    a.child.mutable = foo

    b = a.deepcopy()

    b.child.immutable = 21
    assert a.child.immutable == 42

    b.child.mutable.attribute = False
    assert a.child.mutable.attribute is True

    b.child = "new stuff"
    assert isinstance(a.child, dict_class)


# --- Pickle ---


def test_pickle(dict_class: type[Dict]) -> None:
    a = dict_class(TEST_DICT)
    assert a == pickle.loads(pickle.dumps(a))


# --- Addition ---


def test_add_on_empty_dict(dict_class: type[Dict]) -> None:
    d = dict_class()
    d.x.y += 1
    assert d.x.y == 1


def test_add_on_non_empty_dict(dict_class: type[Dict]) -> None:
    d = dict_class()
    d.x.y = "defined"
    with pytest.raises(TypeError):
        d.x += 1


def test_add_on_non_empty_value(dict_class: type[Dict]) -> None:
    d = dict_class()
    d.x.y = 1
    d.x.y += 1
    assert d.x.y == 2


def test_add_on_unsupported_type(dict_class: type[Dict]) -> None:
    d = dict_class()
    d.x.y = "str"
    with pytest.raises(TypeError):
        d.x.y += 1


# --- Misc ---


def test_init_from_zip(dict_class: type[Dict]) -> None:
    d = dict_class(zip(["a"], [42]))
    assert d.a == 42


def test_setdefault_simple(dict_class: type[Dict]) -> None:
    d = dict_class()
    d.setdefault("a", 2)
    assert d.a == 2
    d.setdefault("a", 3)
    assert d.a == 2
    d.setdefault("c", []).append(2)
    assert d.c == [2]


def test_setdefault_nested(dict_class: type[Dict]) -> None:
    d = dict_class()
    d.one.setdefault("two", [])
    assert d.one.two == []
    d.one.setdefault("three", []).append(3)
    assert d.one.three == [3]


def test_parent_key_item(dict_class: type[Dict]) -> None:
    a = dict_class()
    a["keys"]["x"] = 1
    a[1].x = 3
    assert a == {"keys": {"x": 1}, 1: {"x": 3}}


def test_parent_key_prop(dict_class: type[Dict]) -> None:
    a = dict_class()
    a.y.x = 1
    assert a == {"y": {"x": 1}}


# --- Freeze / Unfreeze ---


def test_top_freeze_against_top_key(dict_class: type[Dict]) -> None:
    d = dict_class()
    assert d.missing == {}
    d.freeze()
    with pytest.raises(KeyError):
        d.missing
    d.unfreeze()
    assert d.missing == {}


def test_top_freeze_against_nested_key(dict_class: type[Dict]) -> None:
    d = dict_class()
    d.inner.present = TEST_VAL
    assert "inner" in d
    assert d.inner.missing == {}
    d.freeze()
    with pytest.raises(KeyError):
        d.inner.missing
    with pytest.raises(KeyError):
        d.missing
    d.unfreeze()
    assert d.inner.missing == {}
    assert d.missing == {}


def test_nested_freeze_against_top_level(dict_class: type[Dict]) -> None:
    d = dict_class()
    d.inner.present = TEST_VAL
    assert d.inner.present == TEST_VAL
    assert d.inner.missing == {}
    assert d.missing == {}
    d.inner.freeze()
    with pytest.raises(KeyError):
        d.inner.missing  # d.inner is frozen
    assert d.missing == {}  # but not `d` itself
    d.inner.unfreeze()
    assert d.inner.missing == {}


def test_top_freeze_disallows_new_key_addition(dict_class: type[Dict]) -> None:
    d = dict_class({"oldKey": None})
    d.freeze()
    d.oldKey = TEST_VAL  # Can set pre-existing key.
    assert d.oldKey == TEST_VAL
    with pytest.raises(KeyError):
        d.newKey = TEST_VAL  # But can't add a new key.
    assert "newKey" not in d
    d.unfreeze()
    d.newKey = TEST_VAL
    assert d.newKey == TEST_VAL
