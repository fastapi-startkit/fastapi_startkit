from fastapi_startkit.fastapi.testing import HttpTestCase


class TestCase(HttpTestCase):
    def get_application(self):
        from bootstrap.application import app

        return app
