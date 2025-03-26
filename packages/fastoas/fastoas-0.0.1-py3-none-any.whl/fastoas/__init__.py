from collections.abc import Sequence
from typing import Any
from typing import Callable


class OpenAPI:
    def __init__(self, app: Any, handlers: Sequence[Callable] = ()) -> None:
        self.app = app
        self.handlers = handlers

    def generate(self) -> dict:
        schema = self.app.__class__.openapi(self.app)
        for handler in self.handlers:
            _, schema = handler(self.app, schema)
        return schema

    def __call__(self) -> dict:
        return self.generate()


__all__ = ["OpenAPI"]
