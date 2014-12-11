# addict - the Python Dict that you'll love more than r/cats.

addict is a Python package that gives you a dictionary who's keys are BOTH gettable and settable using the get- and set attribute syntax, as well as the get- and setitem syntax. This is awesome because you may do the following:

```Python
>>> from addict import Dict
>>> my_new_shiny_dict = Dict()
>>> my_new_shiny_dict.a.b.c.d.e = 2
>>> my_new_shiny_dict
{'a': {'b': {'c': 'd': {'e': 2}}}}
```
It behaves much like a defaultdict, in the way that trying to get a nonexistent key will return a new Dict instance. As ```int```s are not valid attribute names, keys of the dict that are not strings must be set/get with the get-/setitem syntax
```Python
>>> my_new_shiny_dict[2] = [1, 2, 3]
{2: [1, 2, 3], 'a': {'b': {'c': 'd': {'e': 2}}}}
```
You may also mix the two syntaxes:
```Python
>>> my_new_shiny_dict.a.b['c'].d.e
2
```
When is this **especially** useful? 

This package rose from the entirely tiresome creation of elasticsearch queries. When you before were writing something like
```Python
body = {}
filtered = {'filtered': {'query': {}, 'filter': {}}}
filtered['filtered']['query'] = {'match': {'title: 'Mats'}}
filtered['filtered']['filter'] = {'range': 'created_at': {'to': 'now-1d', 'from': 'now-8d'}}
my_hist = {'field': 'created_at', 'interval': '1d', 'min_doc_count': 0}
aggs = {'my_agg': {'date_histogram': my_hist}}
body['query'] = filtered
body[aggs] = aggs

```
You can now write something like this
```Python
body = Dict()
body.query.filtered.query.match.title = 'Mats'
body.query.filtered.filter.range.created_at = {'from': 'now-8d', 'to': 'now-1d'}
my_hist = {'field': 'created_at', 'interval': '1d', 'min_doc_count': 0}
body.aggs.my_agg.date_histogram = my_hist
```

As it is essentially a ```dict```, it will also serialize into JSON perfectly. Ready for use with hopefully all other libraries. If you by mistake added some empty Dicts in your Dict, you can recursively delete those by running .prune() on your Dict.
```Python
>>> a = Dict()
>>> a.a = 2
>>> a.b.c.d.e
{}
>>> a
{'a': 2, 'b': {'c': 'd': {'e': {}}}}
>>> a.prune()
{'a': 2}
```
Could be useful, for example when constructing queries!
