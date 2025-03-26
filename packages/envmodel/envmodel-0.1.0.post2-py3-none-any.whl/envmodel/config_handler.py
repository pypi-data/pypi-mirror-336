from typing import Any

from envmodel.fields import BaseField


class EnvModel:
    def __init__(self, lazy=False):
        self.lazy = lazy
        if not self.lazy:
            self._touch_all_attributes()

    def _touch_all_attributes(self):
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, BaseField):
                field()

    def __getattribute__(self, item: Any) -> Any:
        if isinstance(object.__getattribute__(self, item), BaseField):
            return object.__getattribute__(self, item)()
        return object.__getattribute__(self, item)
