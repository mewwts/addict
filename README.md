# bigdict - the Python dict with the big D.

bigdict is a Python package that gives you a dictionary who's keys are BOTH gettable and settable using the get- and set attribute syntax, as well as the get- and setitem syntax. This is awesome because you may do the following:

```Python
>>> from bigdict import Dict
>>> my_new_shiny_dict = Dict()
>>> my_new_shiny_dict.a.b.c.d.e = 2
>>> my_new_shiny_dict
{'a': {'b': {'c': 'd': {'e': 2}}}}
>>>
>>> my_new_shiny_dict.a.b['c'].d.e
2
>>>
```
It behaves much like a defaultdict, in the way that trying to get a nonexistent key will return a new Dict instance. As ```int```s are not valid attribute names, keys of the dict that are not strings must be set/get with the get-/setitem syntax
```Python
>>> my_new_shiny_dict[2] = [1, 2, 3]
{2: [1, 2, 3], 'a': {'b': {'c': 'd': {'e': 2}}}}
```


