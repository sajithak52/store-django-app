from base_class.views import ModelFormView
from base_class.views import ModelListView
from base_class.views import DeleteView

from store_management.models import Product

from store_management.forms import ProductModelForm


class ProductModelFormView(ModelFormView):
    form_class = ProductModelForm

    def success(self, form, saved):
        data = {
            "id": saved.id,
            "name": saved.name,
            "image": saved.image.url if saved.image else '',
            "selling_price": saved.selling_price if saved.selling_price else '',
            "stock": saved.stock if saved.stock else 0,
            "disable": saved.disable,
            "category": {
                'id': saved.category.id,
                'name': saved.category.name
            } if saved.category else '',
            "loading_plus": False,
            "loading_minus": False
        }
        self.add('data', data)


class ProductDeleteView(DeleteView):
    model = Product


class ProductListView(ModelListView):
    fields = []

    def get_query(self):
        list_for = self.request.GET.get('type')
        if list_for == 'website':
            return Product.objects.filter(disable=False).order_by('-id')

        return Product.objects.all().order_by('-id')

    def to_json(self, record):
        data = {
            "id": record.id,
            "name": record.name,
            "image": record.image.url if record.image else '',
            "selling_price": record.selling_price if record.selling_price else '',
            "stock": record.stock if record.stock else 0,
            "disable": record.disable,
            "category": {
                'id': record.category.id,
                'name': record.category.name
            } if record.category else '',
            "quantity": 0,
            "loading_plus": False,
            "loading_minus": False
        }
        return data
