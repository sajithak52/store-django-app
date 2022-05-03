from .base_class import BaseClass


class ClassView(BaseClass):

    def process(self, request):
        pass

    def render(self):
        request = self.request

        self.process(request)

        return self.response

    def add(self, key, value=True):
        self.response.add(key, value)

    def get(self, key, default=True):
        return self.response.get(key, default)


