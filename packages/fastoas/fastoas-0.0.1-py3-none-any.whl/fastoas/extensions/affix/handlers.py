import contextlib
from typing import Any

from fastoas import const
from fastoas.utils import specification


def affix(app: Any, openapi: dict, attr: str = "__affix__") -> tuple[Any, dict]:
    if not (schemas := openapi.get(const.SPECIFICATION_COMPONENTS, {}).get(const.SPECIFICATION_COMPONENTS_SCHEMAS, {})):
        return app, openapi

    for route in app.routes:
        if not (model := getattr(route, const.FASTAPI_RESPONSE_MODEL, None)):
            continue

        if not (schema := schemas.get(model.__name__, {})):
            continue

        if not model.__name__ == schema.get(const.SPECIFICATION_COMPONENTS_SCHEMAS_TITLE, None):
            continue

        prefixes, postfixes = [], []

        for inheritance in model.__mro__:
            if inheritance.__name__ not in [const.PYDANTIC_BASEMODEL, model.__name__]:
                if value := getattr(inheritance, attr, None):
                    if value.endswith(const.SYMBOL_COLON):
                        prefixes.append(value[:-1])
                    elif value.startswith(const.SYMBOL_COLON):
                        postfixes.append(value[1:])

        name = f"{const.SYMBOL_EMPTY.join(prefixes)}{model.__name__}{const.SYMBOL_EMPTY.join(postfixes)}"

        schema[const.SPECIFICATION_COMPONENTS_SCHEMAS_TITLE] = name
        schemas[name] = schema

        with contextlib.suppress(KeyError):
            del schemas[model.__name__]

        specification.findrefs(openapi, model.__name__, name)

    return app, openapi


__all__ = ["affix"]
