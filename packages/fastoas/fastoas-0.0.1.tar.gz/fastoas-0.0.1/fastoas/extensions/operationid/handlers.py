from typing import Any

from fastoas import const


def use_route_as_operation_id(app: Any, openapi: dict, exclude: tuple[str] = ()) -> tuple[Any, dict]:
    if not (routes := getattr(app, const.SPECIFICATION_ROUTES, [])):
        return app, openapi

    for route in routes:
        if not (endpoint := getattr(route, const.SPECIFICATION_ENDPOINT, None)):
            continue

        if path := getattr(route, const.FASTAPI_ROUTE_PATH, None):
            if path in exclude:
                continue

        if not (paths := openapi.get(const.SPECIFICATION_PATHS, {})):
            continue

        if not (path := paths.get(path, {})):
            continue

        for method in path:
            path[method][const.SPECIFICATION_OPERATION_ID] = getattr(endpoint, "__name__")

    return app, openapi


__all__ = ["use_route_as_operation_id"]
