from base_class.views import ModelFormView
from base_class.views import ModelListView
from base_class.views import DeleteView
from base_class.views import ClassView

from store_management.models import Category, Product

from store_management.forms import CategoryModelForm


class CategoryModelFormView(ModelFormView):
    form_class = CategoryModelForm

    def success(self, form, saved):
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        print('BASE_DIR : ', BASE_DIR)
        print()
        data = {
            'id': saved.id,
            'name': saved.name
        }
        self.add('data', data)


class CategoryDeleteView(DeleteView):
    model = Category

    def pre_save(self, form):
        instance_value = form.cleaned_data.get(self.instance_field)
        product = Product.objects.filter(category_id=instance_value)

        if product.count() > 0:
            category = product[0].category.name
            self.add('error', True)
            self.add('success', False)
            self.add('message', f"{category} is used in {product.count()} products..!!")
            return False

        return True


class CategoryListView(ModelListView):
    fields = ['id', 'name']

    def get_query(self):
        return Category.objects.all()


class CategoryOptionView(ClassView):
    def process(self, request):
        query = Category.objects.all()

        options = []

        for record in query:
            data = {
                'text': record.name,
                'value': record.id
            }
            options.append(data)

        self.add('data', options)



