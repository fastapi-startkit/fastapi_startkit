# FastAPI StartKit

A modular, Masonite-inspired foundation for building robust FastAPI applications.

## Installation
There are two ways to start this project:

1. Clone the repository directly (recommended): This method comes with a structured setup for managing configurations, commands, and other project essentials.
```shell
git clone https://github.com/fastapi-startkit/fastapi_startkit
```
2. Add the `fastapi-startkit` as a dependency.

```shell
poetry add fastapi-startkit
```

---

## Quick Start

### 1. Application Setup
```python
import os
from fastapi_startkit import Application
from fastapi_startkit.logging.providers import LoggingProvider

# Define your providers
PROVIDERS = [
    (LoggingProvider, {
        'default': 'single',
        'channels': {
            'single': {
                'driver': 'single',
                'level': 'debug',
                'path': 'storage/logs/single.log'
            },
        }
    })
]

# Initialize the application
base_path = os.getcwd()
app = Application(base_path, providers=PROVIDERS)
```

### 2. Define Routes

You can define routes using the standard FastAPI instance exposed by the application.

```python
from bootstrap import app

@app.get('/')
def index():
    # Access the container via the application instance if needed, 
    # or just use standard FastAPI features.
    app.make('logger').info('Hello')
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
