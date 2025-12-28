class Facade(type):
    def __getattr__(self, attribute, *args, **kwargs):
        from ..application import app
        return getattr(app().make(self.key), attribute)
