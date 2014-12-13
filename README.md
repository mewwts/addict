# addict - the Python Dict that's better than heroin.
[![build Status](https://travis-ci.org/mewwts/addict.svg?branch=master)](https://travis-ci.org/mewwts/addict) [![Coverage Status](https://img.shields.io/coveralls/mewwts/addict.svg)](https://coveralls.io/r/mewwts/addict)

addict is a Python module that gives you a dictionary whose values are both gettable and settable using both attribute and getitem syntax.

**Never again will you have to write code like this**:
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
From now on, you may simply write the following three lines:
```Python
body = Dict()
body.query.filtered.query.match.description = 'addictive'
body.query.filtered.filter.term.created_by = 'Mats'
```

###Installing
To install simply type
```sh
pip install addict
```
###Usage
addict inherits from ```dict```, but is way more flexible in terms of accessing and setting its values.
Working with dictionaries have never been more awesome than this! Setting the items of a nested Dict is a *dream*:

```Python
>>> from addict import Dict
>>> my_new_shiny_dict = Dict()
>>> my_new_shiny_dict.a.b.c.d.e = 2
>>> my_new_shiny_dict
{'a': {'b': {'c': {'d': {'e': 2}}}}}
```

###Pruning
It behaves much like a defaultdict, in the way that trying to get a nonexistent key will return a new, empty Dict instance.
So trying to peek at an empty item will result in
```Python
>>> my_dict = Dict()
>>> my_dict.a = 2
>>> my_dict.b.c.d.e
{}
>>> my_dict
{'a': 2, 'b': {'c': {'d': {'e': {}}}}}
```
But don't you worry, if you by mistake added some empty Dicts in your Dict, you can recursively delete those by running .prune() on your Dict
```Python
>>> my_dict.prune()
{'a': 2}
```

Also, remember that ```int```s are not valid attribute names, so keys of the dict that are not strings must be set/get with the get-/setitem syntax
```Python
>>> my_other_shiny_dict = Dict()
>>> my_other_shiny_dict.a.b.c.d.e = 2
>>> my_other_shiny_dict[2] = [1, 2, 3]
{2: [1, 2, 3], 'a': {'b': {'c': {'d': {'e': 2}}}}}
```
However feel free to mix the two syntaxes:
```Python
>>> my_other_shiny_dict.a.b['c'].d.e
2
```
###When is this **especially** useful? 

This module rose from the entirely tiresome creation of elasticsearch queries in Python. Whenever you find yourself writing out dicts over multiple lines, just remember that you don't have to. Use a *Dict* instead.

###Perks
As it is essentially a ```dict```, it will also serialize into JSON perfectly. Ready for use with hopefully all other libraries that handles dicts.

###Testimonials
@spiritsack - *"Mother of God, this changes everything."*
