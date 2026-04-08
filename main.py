from bootstrap.app import app

@app.get('/')
async def index():
    app.make('logger').info('Hello')
    return app.make('config').get('logging')
