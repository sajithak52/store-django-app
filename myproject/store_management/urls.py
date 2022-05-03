from django.urls import path

from .views import CategoryModelFormView
from .views import CategoryDeleteView
from .views import CategoryListView
from .views import CategoryOptionView

from .views import ProductModelFormView
from .views import ProductDeleteView
from .views import ProductListView


urlpatterns = [
    CategoryModelFormView.url('category/add-edit/', 'category-add-edit'),
    CategoryDeleteView.url('category/delete/', 'category-delete'),
    CategoryListView.url('category/list/', 'category-list'),
    CategoryOptionView.url('category/options/', 'category-options'),
]

urlpatterns += [
    ProductModelFormView.url('product/add-edit/', 'product-add-edit'),
    ProductDeleteView.url('product/delete/', 'product-delete'),
    ProductListView.url('product/list/', 'product-list'),
]
