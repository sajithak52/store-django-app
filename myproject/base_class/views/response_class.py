from django.conf import settings
from django.http import HttpResponse


class JSONResponse(HttpResponse):

    def __init__(self):
        mimetype = 'application/json'
        HttpResponse.__init__(self, content_type=mimetype)

        self.data = {}
        self.json_string = None

    def add(self, key, value=True):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def render(self):
        return self

    def to_str(self, indent=None):
        from json import dumps

        if indent is None:
            if settings.DEBUG is True:
                indent = 4

        if self.json_string is not None:
            return self.json_string

        s = dumps(self.data, indent=indent)

        self.json_string = s

        return s

    @property
    def content(self):
        return self.make_bytes(self.to_str())

    @content.setter
    def content(self, value):
        pass

    def write(self, content):
        raise Exception("Write is not supported in JSON Response")

    def __iter__(self):
        return iter([self.content])


