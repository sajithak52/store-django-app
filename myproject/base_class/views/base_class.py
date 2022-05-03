from .response_class import JSONResponse


class BaseClass(object):

    def __init__(self, request):
        self.request = request
        self.response = JSONResponse()
        self.params = {}
        self.args = []

    def render(self):
        raise NotImplementedError()

    def post_value(self, *params):
        data = self.request.POST.get
        result = []
        for p in params:
            value = data(p)
            result.append(value)

        if len(result) == 1:
            return result[0]

        return result

    def get_value(self, *params):
        data = self.request.GET.get
        result = []
        for p in params:
            value = data(p)
            result.append(value)

        if len(result) == 1:
            return result[0]

        return result

    @classmethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            obj = cls(request)
            obj.args = args
            obj.params = kwargs
            return obj.render()

        from django.views.decorators.csrf import csrf_exempt

        return csrf_exempt(view)

    @classmethod
    def url(cls, regex, name=None, kwargs=None):
        from django.urls import re_path

        regex = "^{}$".format(regex)

        url = re_path(regex, cls.as_view(), name=name, kwargs=kwargs)
        return url


