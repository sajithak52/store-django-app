from django import forms

from .form_view import FormView


class InstanceForm(forms.Form):
    id = forms.IntegerField()


class DeleteView(FormView):
    form_class = InstanceForm
    model = None
    instance_field = "id"

    def pre_save(self, form):
        return True

    def save(self, form):
        go_through = self.pre_save(form)
        if go_through:
            instance_value = form.cleaned_data.get(self.instance_field)
            model = self.model

            try:
                instance = model.objects.get(**{self.instance_field: instance_value})
            except model.DoesNotExist:
                self.add("error")
                self.add("success", False)
                self.add("message", f"{model.__name__} dose not exist")
            else:
                name = str(instance)
                instance.delete()
                self.add("error", False)
                self.add("success")
                self.add("message", f"{name} is deleted")

