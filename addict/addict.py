from inspect import isgenerator


class Dict(dict):
    """
    Dict is a subclass of dict, which allows you to get AND SET(!!)
    items in the dict using the attribute syntax!

    When you previously had to write:

    my_dict = {'a': {'b': {'c': [1, 2, 3]}}}

    you can now do the same simply by:

    my_Dict = Dict()
    my_Dict.a.b.c = [1, 2, 3]

    Or for instance, if you'd like to add some additional stuff,
    where you'd with the normal dict would write

    my_dict['a']['b']['d'] = [4, 5, 6],

    you may now do the AWESOME

    my_Dict.a.b.d = [4, 5, 6]

    instead. But hey, you can always use the same syntax as a regular dict,
    however, this will not raise TypeErrors or AtrributeErrors at any time
    while you try to get an item. A lot like a defaultdict.

    """
    def __init__(self, *args, **kwargs):
        """
        If we're initialized with a dict, make sure we turn all the
        subdicts into Dicts as well.

        """
        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    self[key] = val
            elif isinstance(arg, list) or isgenerator(arg):
                for key, val in arg:
                    self[key] = val
            elif isinstance(arg, tuple):
                self[arg[0]] = arg[1]
            else:
                raise TypeError("Dict does not understand "
                                "{0} types".format(type(arg)))

        for key, val in kwargs.items():
            self[key] = val

    def __setattr__(self, name, value):
        """
        setattr is called when the syntax a.b = 2 is used to set a value.

        """
        if hasattr(Dict, name):
            raise AttributeError("'Dict' object attribute "
                                 "'{0}' is read-only".format(name))
        else:
            self[name] = value

    def __setitem__(self, name, value):
        """
        This is called when trying to set a value of the Dict using [].
        E.g. some_instance_of_Dict['b'] = val. If 'val

        """
        if isinstance(value, dict):
            value = self.__class__(value)
        super(Dict, self).__setitem__(name, value)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __getitem__(self, name):
        """
        This is called when the Dict is accessed by []. E.g.
        some_instance_of_Dict['a'];
        If the name is in the dict, we return it. Otherwise we set both
        the attr and item to a new instance of Dict.

        """
        if name not in self:
            self[name] = {}
        return super(Dict, self).__getitem__(name)

    def __delattr__(self, name):
        """
        Is invoked when del some_instance_of_Dict.b is called.

        """
        del self[name]

    def __dir__(self):
        """
        Is invoked on a Dict instance causes __getitem__() to get invoked
        which in this module will trigger the creation of the following
        properties: `__members__` and `__methods__`

        To avoid these keys from being added, we simply return an explicit
        call to dir for the Dict object
        """
        return dir(Dict)

    def _ipython_display_(self):
        print(str(self))    # pragma: no cover

    def _repr_html_(self):
        return str(self)

    def _prune(self, prune_zero=False, prune_empty_list=True):
        """
        Recursively remove falsy items from the Dict.

        """
        for key, val in list(self.items()):
            if ((not val) and ((val != 0) or prune_zero) and
                    not isinstance(val, list)):
                del self[key]
            elif isinstance(val, Dict):
                val._prune(prune_zero, prune_empty_list)
                if not val:
                    del self[key]
            elif isinstance(val, list):
                new_list = self._prune_list(val, prune_zero, prune_empty_list)
                if (not new_list) and prune_empty_list:
                    del self[key]
                else:
                    self[key] = new_list

    @classmethod
    def _prune_list(cls, some_list, prune_zero=False, prune_empty_list=True):
        return [x for x in some_list if
                cls._list_reduce(x, prune_zero, prune_empty_list)]

    @classmethod
    def _list_reduce(cls, item, prune_zero=False, prune_empty_list=True):
        if not item:
            return False
        elif isinstance(item, Dict):
            item.prune(prune_zero, prune_empty_list)
            if not item:
                return False
        elif isinstance(item, list):
            new_item = cls._prune_list(item, prune_zero, prune_empty_list)
            if not new_item and prune_empty_list:
                return False
        return True


    def prune(self, prune_zero=False, prune_empty_list=True):
        """
        Removes all empty Dicts and falsy stuff inside the Dict.
        E.g
        >>> a = Dict()
        >>> a.b.c.d
        {}
        >>> a.a = 2
        >>> a
        {'a': 2, 'b': {'c': {'d': {}}}}
        >>> a.prune()
        >>> a
        {'a': 2}

        Set prune_zero=True to remove 0 values
        E.g
        >>> a = Dict()
        >>> a.b.c.d = 0
        >>> a.prune(prune_zero=True)
        >>> a
        {}

        Set prune_empty_list=False to have them persist
        E.g
        >>> a = Dict({'a': []})
        >>> a.prune()
        >>> a
        {}
        >>> a = Dict({'a': []})
        >>> a.prune(prune_empty_list=False)
        >>> a
        {'a': []}
        """
        self._prune(prune_zero, prune_empty_list)
