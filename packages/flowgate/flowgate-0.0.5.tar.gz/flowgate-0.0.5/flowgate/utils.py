from copy import deepcopy
from importlib import import_module
from typing import Any, Callable, List


def import_backend(location: str) -> Any:
    module_name, class_name = location.rsplit(".", 1)
    module = import_module(f"{module_name}")

    backend_cls = getattr(module, class_name)
    return backend_cls


def get_all_nested_keys(data: dict, current_keys: List) -> List:
    all_keys = deepcopy(current_keys)
    if isinstance(data, dict):
        all_keys.extend(list(data.keys()))
        for key, value in data.items():
            if key == "py/object":
                all_keys.append(value)
            else:
                all_keys = get_all_nested_keys(value, all_keys)
    elif isinstance(data, (list, tuple)):
        for item in data:
            all_keys = get_all_nested_keys(item, all_keys)

    return all_keys


def get_callable_representation(target: Callable) -> str:
    return getattr(target, "__qualname__", getattr(target, "__name__", ""))
