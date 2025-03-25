"""Store and modify global app state in JSON (Python dictionary) to re-render front-end components."""

from collections.abc import Callable, Hashable, Iterable, Iterator, MutableMapping
from typing import Any, SupportsIndex, overload

__version__ = '0.0.6'


class DictState(dict):
    def __init__(self, json_state: dict | MutableMapping, *args, **kwargs) -> None:
        self.on_change_callbacks = {}

        # Convert all nested JSON to State
        if isinstance(json_state, dict | MutableMapping):
            for key in json_state:
                value = json_state[key]
                if isinstance(value, dict | MutableMapping | list):
                    json_state[key] = State(value)

        super().__init__(json_state, *args, **kwargs)

    def callbacks(self, key: str) -> list[Callable]:
        self.on_change_callbacks.setdefault(key, [])
        return self.on_change_callbacks[key]

    def pop(
        self, key: Any, default: Any | None = None, /, *args, **kwargs
    ) -> Any | None:
        if key not in self:
            return super().pop(key, default, *args, **kwargs)

        old_value = self[key]
        result = super().pop(key, default, *args, **kwargs)
        for callback in self.on_change_callbacks.get(key, []):
            callback(old_value=old_value, action='remove')
        return result

    def popitem(self) -> tuple[Any, Any]:
        result = super().popitem()
        if result:
            key = result[0]
            old_value = result[1]
            for callback in self.on_change_callbacks.get(key, []):
                callback(old_value=old_value, action='remove')
        return result

    def clear(self) -> None:
        for key in self:
            for callback in self.on_change_callbacks.get(key, []):
                callback(old_value=self[key], action='remove')
        return super().clear()

    @overload
    def update(self, arg: MutableMapping[Hashable, Any], /, **kwargs: Any) -> None: ...

    @overload
    def update(self, arg: Iterable[tuple[Hashable, Any]], /, **kwargs: Any) -> None: ...

    @overload
    def update(self, /, **kwargs: Any) -> None: ...

    def update(self, arg: Any = None, /, **kwargs: Any) -> None:  # type: ignore
        if hasattr(arg, 'keys'):
            for key in arg:
                # TODO: do not send update callbacks if old and new values are the same.
                new_value = arg[key]
                callback_kwargs = None
                if key in self:
                    old_value = self[key]
                    if old_value != new_value:
                        callback_kwargs = {
                            'new_value': new_value,
                            'old_value': old_value,
                            'action': 'update',
                        }
                else:
                    callback_kwargs = {
                        'new_value': new_value,
                        'action': 'add',
                    }

                if callback_kwargs:
                    for callback in self.on_change_callbacks.get(key, []):
                        callback(**callback_kwargs)

            return super().update(arg, **kwargs)
        if arg:
            for key, value in arg:
                new_value = value
                callback_kwargs = None
                if key in self:
                    old_value = self[key]
                    if old_value != new_value:
                        callback_kwargs = {
                            'new_value': new_value,
                            'old_value': old_value,
                            'action': 'update',
                        }
                else:
                    callback_kwargs = {
                        'new_value': new_value,
                        'action': 'add',
                    }

                if callback_kwargs:
                    for callback in self.on_change_callbacks.get(key, []):
                        callback(**callback_kwargs)
            return super().update(arg, **kwargs)
        for key, value in kwargs.items():
            new_value = value
            callback_kwargs = None
            if key in self:
                old_value = self[key]
                if old_value != new_value:
                    callback_kwargs = {
                        'new_value': new_value,
                        'old_value': old_value,
                        'action': 'update',
                    }
            else:
                callback_kwargs = {
                    'new_value': new_value,
                    'action': 'add',
                }

            if callback_kwargs:
                for callback in self.on_change_callbacks.get(key, []):
                    callback(**callback_kwargs)

        return super().update(kwargs, **kwargs)

    def setdefault(self, key, default: Any | None = None, /) -> Any | None:
        callback_kwargs = None
        if key not in self:
            callback_kwargs = {
                'action': 'add',
            }

        result = super().setdefault(key, default)

        if callback_kwargs:
            for callback in self.on_change_callbacks.get(key, []):
                callback(new_value=result, **callback_kwargs)

        return result

    def __setitem__(self, key: Any, value: Any, /, *args, **kwargs) -> None:
        callback_kwargs = None
        new_value = value
        if key in self:
            old_value = self[key]
            if old_value != new_value:
                callback_kwargs = {
                    'new_value': new_value,
                    'old_value': self[key],
                    'action': 'update',
                }
        else:
            callback_kwargs = {
                'new_value': new_value,
                'action': 'add',
            }

        result = super().__setitem__(key, value, *args, **kwargs)

        if callback_kwargs:
            for callback in self.on_change_callbacks.get(key, []):
                callback(**callback_kwargs)

        return result

    def __delitem__(self, key: Any, /) -> None:
        if key not in self:
            return super().__delitem__(key)

        old_value = self[key]
        result = super().__delitem__(key)
        for callback in self.on_change_callbacks.get(key, []):
            callback(old_value=old_value, action='remove')
        return result


class ListState(list):
    """Events emitted:
    add - element is added to a list.
    remove - element is removed from the list.
    update - element is replaced.
    order - place of an element in list is changed.  When element is removed - the event wont be emitted.
    """

    def __init__(self, json_state: list, *args, **kwargs) -> None:
        self.on_change_callbacks = []

        # Convert all nested JSON to State
        if isinstance(json_state, list):
            for index, value in enumerate(json_state):
                if isinstance(value, dict | MutableMapping | list):
                    json_state[index] = State(value)

        super().__init__(json_state, *args, **kwargs)

    def callbacks(self) -> list[Callable]:
        return self.on_change_callbacks

    def append(self, object: Any, /, **kwargs) -> None:
        super().append(object)
        for callback in self.on_change_callbacks:
            callback(new_value=object, action='add')

    def __setitem__(
        self, key: SupportsIndex, value: Any | Iterator[Any], /, **kwargs
    ) -> None:  # type: ignore
        old_value = self[key]
        super().__setitem__(key, value, **kwargs)
        # TODO: check if this key is in a list
        for callback in self.on_change_callbacks:
            callback(new_value=value, old_value=old_value, action='update')

    def __delitem__(self, key: SupportsIndex | slice, /, **kwargs) -> None:
        old_value = self[key]
        # TODO: check if the key is in the list
        # TODO: support slice
        super().__delitem__(key, **kwargs)
        for callback in self.on_change_callbacks:
            callback(old_value=old_value, action='remove')

    def pop(self, index: SupportsIndex = -1, /, **kwargs) -> None:
        # TODO: check if this index is in a list
        old_value = self[index]
        super().pop(index, **kwargs)
        for callback in self.on_change_callbacks:
            callback(old_value=old_value, action='remove')

    def extend(self, iterable, /, **kwargs) -> None:
        elements = list(iterable)
        super().extend(elements, **kwargs)
        for element in elements:
            for callback in self.on_change_callbacks:
                callback(new_value=element, action='add')

    def insert(self, index: SupportsIndex, object: Any, /, **kwargs) -> None:
        super().insert(index, object, **kwargs)
        for callback in self.on_change_callbacks:
            callback(
                new_value=object, action='add', index=index
            )  # TODO: add `index` argument for list updates. Index changes should also be observable.

    def remove(self, value: Any, /, **kwargs) -> None:
        is_value_in_list = value in self
        super().remove(value, **kwargs)
        if is_value_in_list:
            for callback in self.on_change_callbacks:
                callback(old_value=value, action='remove')

    def clear(self) -> None:
        for element in self:
            for callback in self.on_change_callbacks:
                callback(old_value=element, action='remove')

        super().clear()

    # TODO: support ordering: update the index, action="order", value=<current_value>, index- element index in the list.

    def reverse(self) -> None:
        super().reverse()

    def __reversed__(self) -> Iterator[Any]:
        return super().__reversed__()

    def sort(self, *, key: Any | None = None, reverse: bool = False) -> None:
        super().sort(key=key, reverse=reverse)

    def copy(self) -> list[Any]:
        return super().copy()


class SetState(set):
    # TODO: add implementation
    pass


class State(type):
    def __new__(
        cls, json_state: dict | list, *args, **kwargs
    ) -> DictState | ListState | SetState:
        if isinstance(json_state, dict):
            return DictState(json_state)
        if isinstance(json_state, list):
            return ListState(json_state)
        if isinstance(json_state, set):
            return SetState(json_state)
        return None
