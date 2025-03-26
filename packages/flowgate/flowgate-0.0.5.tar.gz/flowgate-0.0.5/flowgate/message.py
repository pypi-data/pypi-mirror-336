import copy
from typing import Callable

try:
    from cnamedtuple import namedtuple
except ImportError:
    from collections import namedtuple


class Message:
    def __init__(self, **kwargs) -> None:
        self.__dict__["_wrapped"] = self._wrapped(**kwargs)

    @property
    def _class(self) -> str:
        return self._wrapped.__class__.__name__

    def to_dict(self) -> dict:
        return self._wrapped._asdict()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        return repr(self._wrapped)

    def __setattr__(self, *args) -> None:
        raise AttributeError("Messages are read only")

    def __getattr__(self, name: str) -> Callable:
        raise NotImplementedError


class NewMessage(Message):
    def __getattr__(self, name: str) -> Callable:
        attr = getattr(self._wrapped, name)
        return copy.deepcopy(attr)


class OldMessage(Message):
    def __getattr__(self, name: str) -> Callable:
        attr = getattr(self._wrapped, name, None)
        return copy.deepcopy(attr)


def message_factory(message_cls: namedtuple, is_new=True) -> type:
    proxy_cls = NewMessage if is_new else OldMessage
    proxy = type(message_cls.__name__, (proxy_cls, object), {"_wrapped": message_cls})
    return proxy


Event = lambda message: message_factory(message)
Command = lambda message: message_factory(message)
