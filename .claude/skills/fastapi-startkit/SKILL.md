---
name: fastapi-startkit
description: Routing, controllers, ORM, requests, resources, and action pattern for fastapi-startkit applications.
---

# Fastapi's Routing

### Fastapi Startkit's Router
```python
# routes/web.py
from fastapi_startkit.fastapi import Router

router = Router()
```

and use the crud resources, for example
```python
router.post("/users", users_controller.store)
router.put("/users/{user_id}", users_controller.update)
router.patch("/users/{user_id}", users_controller.patch)
router.delete("/users", users_controller.destroy)
```

the controller will look like
```python
# app/http/controllers/users_controller.py
async def index(request: Request):
    pass

async def show(user_id: int):
    pass

async def store(data: UserSchema):
    pass

async def update(user_id: int, data: UserSchema):
    pass

async def destroy(user_id: int):
    pass
```

or use the resource function as:
```python
router.resource("users", users_controller, excepts=['create', 'edit'])
```

## ORM
```python
# app/models/user.py
from fastapi_startkit.masoniteorm import Model

class User(Model):
    id: int
    name: str
    email: str
    metadata: dict
```

and use the orm as:
```python
# app/http/controllers/users_controller.py
from app.models import User

async def store(request: UserStoreRequest):
    user = User.create(request.model_dump())
    ...
```

the `UserStoreRequest` will look like:
```python
# app/http/requests/user_store_request.py
from pydantic import BaseModel

class UserStoreRequest(BaseModel):
    name: str
```

and use JsonApiResource to return JSON response from the controller:
```python
from fastapi_startkit.jsonapi import JsonResource

# app/http/controllers/users_controller.py
from app.models import User

async def store(request: UserStoreRequest):
    user = User.create(request.model_dump())
    return JsonResource(user)
```

## Architecture

use the action pattern to write complex logic.
```python
# app/actions/user_actions.py
from app.models import User

class UserStoreAction:
    def __init__(self, request: UserStoreRequest):
        self.request = request

    @staticmethod
    def prepare(request: UserStoreRequest) -> 'UserStoreAction':
        return UserStoreAction(request)

    def handle(self) -> JsonResource[User]:
        user = User.create(self.request.model_dump())
        return JsonResource(user)
```
