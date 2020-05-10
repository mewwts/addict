import copy


class Dict(dict):

    def __init__(__self, *args, **kwargs):
        object.__setattr__(__self, '__parent', kwargs.pop('__parent', None))
        object.__setattr__(__self, '__key', kwargs.pop('__key', None))
        object.__setattr__(__self, '__frozen', False)
        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    __self[key] = __self._hook(val)
            elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
                __self[arg[0]] = __self._hook(arg[1])
            else:
                for key, val in iter(arg):
                    __self[key] = __self._hook(val)

        for key, val in kwargs.items():
            __self[key] = __self._hook(val)

    def __setattr__(self, name, value):
        if hasattr(self.__class__, name):
            raise AttributeError("'Dict' object attribute "
                                 "'{0}' is read-only".format(name))
        else:
            self[name] = value

    def __setitem__(self, name, value):
        if isinstance(name, str) and '.' in name:
            name_split = name.rsplit('.', 1)
            self[name_split[0]][name_split[1]]=value
            return#+
        ## superfreezing prevents the creation of new keys (but modification is still possible)
        ## without this two lines, freezing only prevents the reaction of intermediate keys
        if hasattr(self,'__frozen') and object.__getattribute__(self, '__frozen') and name not in super().keys():
            raise KeyError(name)
        super(Dict, self).__setitem__(name, value)
        try:
            p = object.__getattribute__(self, '__parent')
            key = object.__getattribute__(self, '__key')
        except AttributeError:
            p = None
            key = None
        if p is not None:
            p[key] = self
            object.__delattr__(self, '__parent')
            object.__delattr__(self, '__key')

    def __add__(self, other):
        if not self.keys():
            return other
        else:
            self_type = type(self).__name__
            other_type = type(other).__name__
            msg = "unsupported operand type(s) for +: '{}' and '{}'"
            raise TypeError(msg.format(self_type, other_type))

    @classmethod
    def _hook(cls, item):
        if isinstance(item, dict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __getitem__(self, name):
        if isinstance(name, str) and '.' in name:
            name_split = name.split('.', 1)
            return self[name_split[0]][name_split[1]]
        else:
            return super().__getitem__(name)

    def __missing__(self, name):
        if not object.__getattribute__(self,'__frozen'):
            return self.__class__(__parent=self, __key=name)
        raise KeyError(name)

    def __delattr__(self, name):
        del self[name]

    def to_dict(self):
        base = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else
                    item for item in value)
            else:
                base[key] = value
        return base

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        other = self.__class__()
        memo[id(self)] = other
        for key, value in self.items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def update(self, *args, **kwargs):
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError()
            other.update(args[0])
        other.update(kwargs)
        for k, v in other.items():
            if ((k not in self) or
                (not isinstance(self[k], dict)) or
                (not isinstance(v, dict))):
                self[k] = v
            else:
                self[k].update(v)

    def __getnewargs__(self):
        return tuple(self.items())

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def get(self, key, default=None):
        #if the dict is not frozen, d.get returns an empty dict in case of non existing key
        #so we must take care of preserving freeze state
        frozen=object.__getattribute__(self,'__frozen')
        if not frozen:
            self.freeze()
        try:
            res= self.__getitem__(key)
        except:
            res= default
        if not frozen:
            self.unfreeze()
        return res

    def freeze(__self):
        object.__setattr__(__self,'__frozen',True)
        for k in __self.keys():
            try:
                __self[k].freeze()
            except:
                pass
        return __self

    def unfreeze(__self):
        object.__setattr__(__self,'__frozen',False)
        for k in __self.keys():
            try:
                __self[k].unfreeze()
            except:
                pass
        return __self
