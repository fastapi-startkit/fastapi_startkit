from fastapi_startkit.logging import Logger

from wsgi import application as app

@app.get('/')
def index():
    app.make('logger').info('Hello')
    return app.make('config').get('logging')
