from fastapi_startkit.providers import Provider


class DatabaseProvider(Provider):
    def register(self):
        config = self.application.make("config")

        from masoniteorm.query import QueryBuilder
        from masoniteorm.connections import ConnectionResolver

        # Register ConnectionResolver
        db_config = config.get("database.databases") or config.get("database")
        resolver = ConnectionResolver().set_connection_details(db_config)
        self.application.bind("resolver", resolver)

        # Register QueryBuilder
        self.application.bind(
            "builder",
            QueryBuilder(connection_details=db_config, connection='default'),
        )

        # Register Migrations and Seeds locations
        self.application.bind("migrations.location", "databases/migrations")
        self.application.bind("seeds.location", "databases/seeds")

    def boot(self):
        pass
