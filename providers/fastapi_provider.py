from fastapi_startkit.fastapi.providers.fastapi_provider import FastAPIProvider as BaseProvider


class FastapiProvider(BaseProvider):
    """Provider for FastAPI framework integration."""

    def register(self):
        from fastapi import FastAPI

        fastapi = FastAPI(
            title="Jobins AI Agent (LangChain)",
            version="1.0.0",
        )

        self.app.use_fastapi(fastapi)

    def boot(self):
        super().boot()
        from routes.api import api

        self.app.fastapi.include_router(api)
