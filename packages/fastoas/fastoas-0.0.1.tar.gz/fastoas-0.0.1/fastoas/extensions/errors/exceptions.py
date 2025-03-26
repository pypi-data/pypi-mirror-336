from http import HTTPStatus


class APIError(Exception):
    status_code: int = HTTPStatus.IM_A_TEAPOT

    def to_dict(self) -> dict:
        return dict(
            status_code=self.status_code,
            detail=dict(type=self.__class__.__name__),
        )


__all__ = ["APIError"]
