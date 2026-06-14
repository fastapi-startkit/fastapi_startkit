from fastapi_startkit.fastapi import FastAPIProvider as BaseFastAPIProvider


class FastapiProvider(BaseFastAPIProvider):
    def boot(self):
        super().boot()
        from routes.api import api

        self.app.fastapi.include_router(api)
