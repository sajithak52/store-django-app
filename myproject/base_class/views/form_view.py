from .base_view import ClassView


class FormView(ClassView):
    form_class = None

    need_request = False

    def __init__(self, request):
        ClassView.__init__(self, request)
        self._form = None

    def _success(self, form):
        self.add("success", True)
        self.add("error", False)

    def _error(self, form):
        self.add("success", False)
        self.add("error", True)
        self.add_form_errors(form)

    def add_form_errors(self, form):
        form_errors = form.errors
        self.add('errors', form_errors)

    def pre_process(self, request):
        pass

    def process(self, request):
        self.pre_process(request)
        form = self.get_form()
        self._form = form

        if self.is_valid(form):
            self.save(form)
            self._success(form)
            self.success(form)
        else:
            self._error(form)

    def get_form_data(self):
        return self.request.POST

    def get_form(self):
        request = self.request
        args = (self.get_form_data(), request.FILES)

        kwargs = {}
        if self.need_request:
            kwargs['request'] = request
        self.form_params(kwargs)
        form = self.form_class(*args, **kwargs)

        return form

    def form_params(self, kwargs):
        pass

    #
    # Hooks
    #
    def is_valid(self, form):
        return form.is_valid()

    def save(self, form):
        pass

    def success(self, form):
        pass


class ModelFormView(FormView):
    instance_model_field = "id"

    instance_form_field = "id"

    def __init__(self, request, instance=None):
        FormView.__init__(self, request)
        self._instance = instance
        self._instance_found = False

    def process(self, request):
        form = self.get_form()
        self._form = form

        if self.is_valid(form):
            saved = self.save(form)
            self._success(form, saved)
            self.success(form, saved)
        else:
            self._error(form)

    def save(self, form):
        return form.save()

    def instance(self):
        if self._instance is not None or self._instance_found:
            return self._instance

        request = self.request
        cls = self.form_class
        meta = getattr(cls, '_meta', None)

        if not meta:
            self._instance_found = True
            return

        model = getattr(meta, 'model', None)
        if not model:
            self._instance_found = True
            return

        form_key = self.instance_form_field
        model_key = self.instance_model_field
        value = request.POST.get(form_key, "")

        if not value:
            self._instance_found = True
            return

        try:
            instance = model.objects.get(**{model_key: value})
            self._instance = instance
            return instance
        except model.DoesNotExist:
            self._instance_found = True
            return

    def get_form(self):
        request = self.request
        args = (request.POST, request.FILES)

        kwargs = {}
        if self.need_request:
            kwargs['request'] = request

        instance = self.instance()
        if instance:
            kwargs['instance'] = instance

        self.form_params(kwargs)

        form = self.form_class(*args, **kwargs)

        return form

    # noinspection PyMethodOverriding
    def _success(self, form, saved):
        FormView._success(self, form)

    # noinspection PyMethodOverriding
    def success(self, form, saved):
        pass

