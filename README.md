# addict
![Tests](https://github.com/mewwts/addict/workflows/Python%20test/badge.svg) [![Coverage Status](https://img.shields.io/coveralls/mewwts/addict.svg)](https://coveralls.io/r/mewwts/addict) [![PyPI version](https://badge.fury.io/py/addict.svg)](https://badge.fury.io/py/addict) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/addict/badges/version.svg)](https://anaconda.org/conda-forge/addict)

addict is a Python module that gives you dictionaries whose values are both gettable and settable using attributes, in addition to standard item-syntax.

This means that you **don't have to** write dictionaries like this anymore:
```Python
body = {
    'query': {
        'filtered': {
            'query': {
                'match': {'description': 'addictive'}
            },
            'filter': {
                'term': {'created_by': 'Mats'}
            }
        }
    }
}
```
Instead, you can simply write the following three lines:
```Python
body = Dict()
body.query.filtered.query.match.description = 'addictive'
body.query.filtered.filter.term.created_by = 'Mats'
```

### Installing
You can install via `pip`
```sh
pip install addict
```

or through `conda`
```sh
conda install addict -c conda-forge
```

Addict runs on Python 2 and Python 3, and every build is tested towards 2.7, 3.6 and 3.7. 

### Usage
addict inherits from ```dict```, but is more flexible in terms of accessing and setting its values.
Working with dictionaries are now a *joy*! Setting the items of a nested Dict is a *dream*:

```Python
>>> from addict import Dict
>>> mapping = Dict()
>>> mapping.a.b.c.d.e = 2
>>> mapping
{'a': {'b': {'c': {'d': {'e': 2}}}}}
```

If the `Dict` is instantiated with any iterable values, it will iterate through and clone these values, and turn `dict`s into `Dict`s.
Hence, the following works
```Python
>>> mapping = {'a': [{'b': 3}, {'b': 3}]}
>>> dictionary = Dict(mapping)
>>> dictionary.a[0].b
3
```
but `mapping['a']` is no longer the same reference as `dictionary['a']`.
```Python
>>> mapping['a'] is dictionary['a']
False
```
This behavior is limited to the constructor, and not when items are set using attribute or item syntax, references are untouched:
```Python
>>> a = Dict()
>>> b = [1, 2, 3]
>>> a.b = b
>>> a.b is b
True
```

### Stuff to keep in mind
Remember that ```int```s are not valid attribute names, so keys of the dict that are not strings must be set/get with the get-/setitem syntax
```Python
>>> addicted = Dict()
>>> addicted.a.b.c.d.e = 2
>>> addicted[2] = [1, 2, 3]
{2: [1, 2, 3], 'a': {'b': {'c': {'d': {'e': 2}}}}}
```
However feel free to mix the two syntaxes:
```Python
>>> addicted.a.b['c'].d.e
2
```

### Attributes like keys, items etc.
addict will not let you override attributes that are native to ```dict```, so the following will not work
```Python
>>> mapping = Dict()
>>> mapping.keys = 2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "addict/addict.py", line 53, in __setattr__
    raise AttributeError("'Dict' object attribute '%s' is read-only" % name)
AttributeError: 'Dict' object attribute 'keys' is read-only
```
However, the following is fine
```Python
>>> a = Dict()
>>> a['keys'] = 2
>>> a
{'keys': 2}
>>> a['keys']
2
```
just like a regular `dict`. There are no restrictions (other than what a regular dict imposes) regarding what keys you can use.

### Default values
For keys that are not in the dictionary, addict behaves like ```defaultdict(Dict)```, so missing keys return an empty ```Dict```
rather than raising ```KeyError```.
If this behaviour is not desired, it can be overridden using
```Python
>>> class DictNoDefault(Dict):
>>>     def __missing__(self, key):
>>>         raise KeyError(key)
```
but beware that you will then lose the shorthand assignment functionality (```addicted.a.b.c.d.e = 2```).

### Recursive Fallback to dict
If you don't feel safe shipping your addict around to other modules, use the `to_dict()`-method, which returns a regular dict clone of the addict dictionary.

```Python
>>> regular_dict = my_addict.to_dict()
>>> regular_dict.a = 2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'a'
```
This is perfect for when you wish to create a nested Dict in a few lines, and then ship it on to a different module. 
```Python
body = Dict()
body.query.filtered.query.match.description = 'addictive'
body.query.filtered.filter.term.created_by = 'Mats'
third_party_module.search(query=body.to_dict())
```

### Counting
`Dict`'s ability to easily access and modify deeply-nested attributes makes it ideal for counting. This offers a distinct advantage over `collections.Counter`, as it will easily allow for counting by multiple levels.

Consider this data:

```python
data = [
    {'born': 1980, 'gender': 'M', 'eyes': 'green'},
    {'born': 1980, 'gender': 'F', 'eyes': 'green'},
    {'born': 1980, 'gender': 'M', 'eyes': 'blue'},
    {'born': 1980, 'gender': 'M', 'eyes': 'green'},
    {'born': 1980, 'gender': 'M', 'eyes': 'green'},
    {'born': 1980, 'gender': 'F', 'eyes': 'blue'},
    {'born': 1981, 'gender': 'M', 'eyes': 'blue'},
    {'born': 1981, 'gender': 'F', 'eyes': 'green'},
    {'born': 1981, 'gender': 'M', 'eyes': 'blue'},
    {'born': 1981, 'gender': 'F', 'eyes': 'blue'},
    {'born': 1981, 'gender': 'M', 'eyes': 'green'},
    {'born': 1981, 'gender': 'F', 'eyes': 'blue'}
]
```

If you want to count how many people were born in `born` of gender `gender` with `eyes` eyes, you can easily calculate this information:

```python
counter = Dict()

for row in data:
    born = row['born']
    gender = row['gender']
    eyes = row['eyes']

    counter[born][gender][eyes] += 1

print(counter)
```

```
{1980: {'M': {'blue': 1, 'green': 3}, 'F': {'blue': 1, 'green': 1}}, 1981: {'M': {'blue': 2, 'green': 1}, 'F': {'blue': 2, 'green': 1}}}
```
### Update
`addict`s update functionality is altered for convenience from a normal `dict`. Where updating nested item using a `dict` would overwrite it:
```Python
>>> d = {'a': {'b': 3}}
>>> d.update({'a': {'c': 4}})
>>> print(d)
{'a': {'c': 4}}
```
`addict` will recurse and _actually_ update the nested `Dict`. 
```Python
>>> D = Dict({'a': {'b': 3}})
>>> D.update({'a': {'c': 4}})
>>> print(D)
{'a': {'b': 3, 'c': 4}}
```

### When is this **especially** useful? 
This module rose from the entirely tiresome creation of Elasticsearch queries in Python. Whenever you find yourself writing out dicts over multiple lines, just remember that you don't have to. Use *addict* instead.

### Perks
As it is a ```dict```, it will serialize into JSON perfectly, and with the to_dict()-method you can feel safe shipping your addict anywhere.

### Testing, Development and CI
Issues and Pull Requests are more than welcome. Feel free to open an issue to spark a discussion around a feature or a bug, or simply reply to the existing ones. As for Pull Requests, keeping in touch with the surrounding code style will be appreciated, and as such, writing tests are crucial. Pull requests and commits will be automatically run against TravisCI and coveralls. 

The unit tests are implemented in the `test_addict.py` file and use the unittest python framework. Running the tests is rather simple:
```sh
python -m unittest -v test_addict

# - or -
python test_addict.py
```

### Testimonials
@spiritsack - *"Mother of God, this changes everything."*

@some guy on Hacker News - *"...the purpose itself is grossly unpythonic"*
