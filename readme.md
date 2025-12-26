# FastAPI StartKit

A modular, Masonite-inspired foundation for building robust FastAPI applications.

## Installation

Install the package via Poetry:

```shell
poetry add fastapi-startkit
```

### Optional Extras
To include database support (Masonite ORM):

```shell
poetry add fastapi-startkit --extras "database"
```

---

## Quick Start

### 1. Application Setup (`wsgi.py` or `main.py`)

No `sys.path` manipulation is required. Import `Application` and your necessary providers directly.

> **Important**: You must explicitly include `ConfigurationProvider` to load configuration files from your `config/` directory.

```python
import os
from fastapi_startkit import Application
from fastapi_startkit_foundation.providers import ConfigurationProvider
from fastapi_startkit_database.providers import DatabaseProvider

# Define your providers
# ConfigurationProvider is required to load your config files.
PROVIDERS = [
    ConfigurationProvider,
    DatabaseProvider,
]

# Initialize the application
# base_path should point to the root where your 'config/' directory exists.
base_path = os.getcwd()
application = Application(base_path, PROVIDERS)
```

### 2. Define Routes

You can define routes using the standard FastAPI instance exposed by the application.

```python
from wsgi import app

@app.get('/')
def index():
    # Access the container via the application instance if needed, 
    # or just use standard FastAPI features.
    return {"message": "Hello World"}
```

---

## Configuration

The `ConfigurationProvider` loads configuration files from the `config/` directory in your `base_path`.

Example `config/database.py`:
```python
from masoniteorm.connections import ConnectionResolver

DATABASES = {
    "default": "sqlite",
    "sqlite": {
        "driver": "sqlite",
        "database": "database.sqlite3",
    }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
```

## Database Usage

With the `ORMProvider` registered, you can use Masonite ORM models normally.

```python
from masoniteorm.models import Model

class User(Model):
    __table__ = "users"

# Querying
users = User.all()
```

### CLI Commands (Artisan)

```shell
# Run Migrations
poetry run python artisan migrate

# Run Seeds
poetry run python artisan seed
```
