from wsgi import application as app


@app.get('/')
def index():
    return app.make('config').get('database.databases')
