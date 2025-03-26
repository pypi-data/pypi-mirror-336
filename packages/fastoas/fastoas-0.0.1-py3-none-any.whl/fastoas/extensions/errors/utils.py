from fastoas import const


def openapi_errors(*args) -> dict:
    errors, grouped = {}, {}

    for error in [arg() for arg in args]:
        if error.status_code not in grouped:
            grouped[error.status_code] = []
        grouped[error.status_code].append(error.to_dict())

    for status_code, examples in grouped.items():
        errors[status_code] = {
            const.SPECIFICATION_PATHS_RESPONSES_CONTENT: {
                const.SPECIFICATION_PATHS_RESPONSES_CONTENT_APPLICATION_JSON: {
                    const.SPECIFICATION_PATHS_RESPONSES_CONTENT_APPLICATION_JSON_EXAMPLE: examples
                    if len(examples) > 1
                    else examples[0]
                }
            }
        }

    return errors


__all__ = ["openapi_errors"]
