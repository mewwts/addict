from __future__ import annotations

import copy
from collections.abc import Iterable
from typing import Any

__all__ = ["Dict"]


class Dict(dict):
    def __init__(__self, *args: Any, **kwargs: Any) -> None:
        object.__setattr__(__self, "__parent", kwargs.pop("__parent", None))
        object.__setattr__(__self, "__key", kwargs.pop("__key", None))
        object.__setattr__(__self, "__frozen", False)
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

    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self.__class__, name):
            raise AttributeError(f"'Dict' object attribute '{name}' is read-only")
        else:
            self[name] = value

    def __setitem__(self, name: Any, value: Any) -> None:
        is_frozen = hasattr(self, "__frozen") and object.__getattribute__(
            self, "__frozen"
        )
        if is_frozen and name not in super().keys():
            raise KeyError(name)
        super().__setitem__(name, value)
        try:
            p = object.__getattribute__(self, "__parent")
            key = object.__getattribute__(self, "__key")
        except AttributeError:
            p = None
            key = None
        if p is not None:
            p[key] = self
            object.__delattr__(self, "__parent")
            object.__delattr__(self, "__key")

    def __add__(self, other: Any) -> Any:
        if not self.keys():
            return other
        else:
            self_type = type(self).__name__
            other_type = type(other).__name__
            raise TypeError(
                f"unsupported operand type(s) for +: '{self_type}' and '{other_type}'"
            )

    @classmethod
    def _hook(cls, item: Any) -> Any:
        if isinstance(item, dict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, item: str) -> Any:
        return self.__getitem__(item)

    def __missing__(self, name: Any) -> Dict:
        if object.__getattribute__(self, "__frozen"):
            raise KeyError(name)
        return self.__class__(__parent=self, __key=name)

    def __delattr__(self, name: str) -> None:
        del self[name]

    def to_dict(self) -> dict[str, Any]:
        base: dict[str, Any] = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else item
                    for item in value
                )
            else:
                base[key] = value
        return base

    def copy(self) -> Dict:
        return copy.copy(self)

    def deepcopy(self) -> Dict:
        return copy.deepcopy(self)

    def __deepcopy__(self, memo: dict[int, Any]) -> Dict:
        other = self.__class__()
        memo[id(self)] = other
        for key, value in self.items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def update(self, *args: Any, **kwargs: Any) -> None:
        other: dict[Any, Any] = {}
        if args:
            if len(args) > 1:
                raise TypeError()
            other.update(args[0])
        other.update(kwargs)
        for k, v in other.items():
            if (
                (k not in self)
                or (not isinstance(self[k], dict))
                or (not isinstance(v, dict))
            ):
                self[k] = v
            else:
                self[k].update(v)

    def __getnewargs__(self) -> tuple[tuple[Any, Any], ...]:
        return tuple(self.items())

    def __getstate__(self) -> dict[Any, Any]:
        return self

    def __setstate__(self, state: dict[Any, Any]) -> None:
        self.update(state)

    def __or__(self, other: dict[Any, Any] | Dict) -> Dict:
        if not isinstance(other, (Dict, dict)):
            return NotImplemented
        new = Dict(self)
        new.update(other)
        return new

    def __ror__(self, other: dict[Any, Any] | Dict) -> Dict:
        if not isinstance(other, (Dict, dict)):
            return NotImplemented
        new = Dict(other)
        new.update(self)
        return new

    def __ior__(self, other: dict[Any, Any] | Dict | Iterable[tuple[Any, Any]]) -> Dict:  # type: ignore[override]
        self.update(other)
        return self

    def setdefault(self, key: Any, default: Any = None) -> Any:
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def freeze(self, should_freeze: bool = True) -> None:
        object.__setattr__(self, "__frozen", should_freeze)
        for _key, val in self.items():
            if isinstance(val, Dict):
                val.freeze(should_freeze)

    def unfreeze(self) -> None:
        self.freeze(False)
