<p align="center">
  <a href="https://github.com/AlexDemure/fastoas">
    <a href="https://ibb.co/SwwDyCsJ"><img src="https://i.ibb.co/jkk9fX6H/Frame-1349-2.png" alt="Frame-1349-2" border="0"></a>
  </a>
</p>

<p align="center">
  Utility toolkit to modify and override OpenAPI schema definitions in FastAPI.
</p>

---

## Installation

```
pip install fastoas
```

## Usage
```
from fastoas import OpenAPI

app.openapi = Fastoas(app)
```

### Extension ```fastoas.extensions.affix```

```
from fastapi import FastAPI
from pydantic import BaseModel

from fastoas import OpenAPI
from fastoas.extensions.affix import affix

app = FastAPI()

app.openapi = OpenAPI(app, handlers=[affix])


class Deprecated(BaseModel):
    __affix__ = "Deprecated:"


class User(Deprecated):
    id: int


@app.get("/user", response_model=User)
def get_user():
    return {"id": 1}

openapi.json
>>>
{
  "paths": {
    "schema": {
      "$ref": "#/components/schemas/DeprecatedUser"
    }
  },
  "schemas": {
      "DeprecatedUser": {
        "title": "DeprecatedUser"
      }
    }
}
```

### Extension ```fastoas.extensions.operationid```

```
from fastapi import FastAPI
from pydantic import BaseModel

from fastoas import OpenAPI
from fastoas.extensions.operationid import use_route_as_operation_id

app = FastAPI()

app.openapi = OpenAPI(app, handlers=[use_route_as_operation_id])


class User(Deprecated):
    id: int


@app.get("/user", response_model=User)
def get_user():
    return {"id": 1}

openapi.json
>>> BEFORE
{
  "paths": {
    "/user": {
      "get": {
        "operationId": "get_user_user_get",
      }
    }
  }
}

>>> AFTER
{
  "paths": {
    "/user": {
      "get": {
        "operationId": "get_user",
      }
    }
  }
}
```

### Extension ```fastoas.extensions.errors``` 

```
from fastapi import FastAPI
from fastoas.extensions.errors import APIError, openapi_errors

app = FastAPI()


class MyError(APIError):
    ...


@app.get("/user", response_model=dict, responses=openapi_errors(MyError))
def get_user():
    return {"id": 1}

openapi.json
>>>
{
  "paths": {
    "/user": {
      "get": {
        "responses": {
          "200": {
            "description": "Successful Response"
          },
          "418": {
            "description": "MyError",
            "content": {
              "application/json": {
                "example": {
                  "status_code": 418,
                  "detail": {
                    "type": "MyError"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```


### Custom handler

```
from fastapi import FastAPI
from fastoas import OpenAPI

def my_handler(app: FastAPI, openapi: dict) -> tuple[FastAPI, dict]:
    # Mutate openapi here
    return app, openapi

app = FastAPI()

app.openapi = OpenAPI(app, handlers=[my_handler])

@app.get("/user", response_model=dict)
def get_user():
    return {"id": 1}
```
