from django import forms

from .models import Category
from .models import Product


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
