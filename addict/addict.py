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
        if (args and isinstance(args[0], dict)):
            for key, val in args[0].items():
                self._set_both(key, val)

    def __setattr__(self, name, value):
        """
        setattr is called when the syntax a.b = 2 is used to set a value.

        """
        self._set_both(name, value)

    def _set_both(self, name, value):
        """
        This method does the 'heavy' lifting here. If value is an instance
        of dict, it will be turned into a Dict (Yay!). If name is a string,
        it can be set as a property. If name is not in the Dict already,
        we put it in :-)

        """
        if isinstance(value, dict):
            value = self.__class__(value)
        if isinstance(name, str):
            super(Dict, self).__setattr__(name, value)
            super(Dict, self).__setitem__(name, value)

    def __setitem__(self, name, value):
        """
        This is called when trying to set a value of the Dict using [].
        E.g. some_instance_of_Dict['b'] = val. If 'val

        """
        self._set_both(name, value)

    def __getattr__(self, name):
        """
        This is called when __getattribute__ can't find an attribute.
        So this only handles the cases of missing attributes. This
        is the defaultdict-like part.

        """
        self._set_both(name, {})
        return super(Dict, self).__getattribute__(name)

    def __getitem__(self, name):
        """
        This is called when the Dict is accessed by []. E.g.
        some_instance_of_Dict['a'];
        If the name is in the dict, we return it. Otherwise we set both
        the attr and item to a new instance of Dict.

        """
        if name in self:
            return super(Dict, self).__getitem__(name)
        else:
            self._set_both(name, {})
            return super(Dict, self).__getitem__(name)

    def __delattr__(self, name):
        """
        Is invoked when del some_instance_of_Dict.b is called.

        """
        self._delete(name)

    def __delitem__(self, name):
        """
        Is invoked when del some_instance_of_Dict[b] is called.

        """
        self._delete(name)

    def _delete(self, name):
        """
        Deletes both the attribute and item associated with 'name'

        """
        super(Dict, self).__delitem__(name)
        super(Dict, self).__delattr__(name)

    def _prune(self):
        """
        Recursively remove falsy items from the Dict.

        """
        for key, val in list(self.items()):
            if (not val) and (val != 0):
                self._delete(key)
            elif isinstance(val, Dict):
                val._prune()
                if not val:
                    self._delete(key)
            elif isinstance(val, list):
                new_list = self._prune_list(val)
                self._set_both(key, new_list)

    @classmethod
    def _prune_list(cls, some_list):
        return [x for x in some_list if cls._list_reduce(x)]

    @classmethod
    def _list_reduce(cls, item):
        if not item:
            return False
        elif isinstance(item, Dict):
            item.prune()
            if not item:
                return False
        elif isinstance(item, list):
            new_item = cls._prune_list(item)
            if not new_item:
                return False
        return True


    def prune(self):
        """
        Removes all empty Dicts and falsy stuff inside the Dict.
        0 vals are allowed for now.
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
        """
        self._prune()
