from masoniteorm.connections import ConnectionResolver

DATABASES = {
    "default": "postgres",
    "mysql": {
        "host": "127.0.0.1",
        "driver": "mysql",
        "database": "masonite",
        "user": "root",
        "password": "",
        "port": 3306,
        "log_queries": False,
        "options": {
            #
        }
    },
    "postgres": {
        "host": "127.0.0.1",
        "driver": "postgres",
        "database": "local",
        "user": "local",
        "password": "secret",
        "port": 5432,
        "log_queries": False,
        "options": {
            #
        }
    },
    "sqlite": {
        "driver": "sqlite",
        "database": "masonite.sqlite3",
    }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
