from base_class.views import ModelFormView
from base_class.views import ClassView
from .forms import StoreManagementModelForm
from .models import StoreManagement


class OpenStoreFormView(ModelFormView):
    form_class = StoreManagementModelForm

    def success(self, form, saved):
        data = {
            'id': saved.id,
            'is_open': saved.is_open
        }
        self.add('data', data)


class CheckShopIsOpen(ClassView):
    def process(self, request):

        obj = StoreManagement.objects.all().order_by('-id')

        if obj.count() > 0:
            saved = obj[0]
            data = {
                'id': saved.id,
                'is_open': saved.is_open
            }
            self.add('error', False)
            self.add('success', True)
            self.add('data', data)

        else:
            saved = StoreManagement.objects.create(is_open=False)
            data = {
                'id': saved.id,
                'is_open': saved.is_open
            }
            self.add('error', False)
            self.add('success', True)
            self.add('data', data)


class CheckShopIsOpenForUser(ClassView):
    def process(self, request):

        obj = StoreManagement.objects.all().order_by('-id')

        if obj.count() > 0:
            saved = obj[0]
            self.add('error', False)
            self.add('success', True)
            self.add('is_open', saved.is_open)

        else:
            self.add('error', False)
            self.add('success', True)
            self.add('is_open', False)

