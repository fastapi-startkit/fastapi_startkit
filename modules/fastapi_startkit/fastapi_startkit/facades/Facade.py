class Facade(type):
    
    application = None

    def __getattr__(self, attribute, *args, **kwargs):
        if self.application:
            return getattr(self.application.make(self.key), attribute)
            
        from wsgi import application

        return getattr(application.make(self.key), attribute)
