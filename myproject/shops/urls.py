from .views import OpenStoreFormView
from .views import CheckShopIsOpen
from .views import CheckShopIsOpenForUser


urlpatterns = [
    OpenStoreFormView.url('open-store/', 'open-store'),
    CheckShopIsOpen.url('check-open-store/', 'check-open-store'),
    CheckShopIsOpenForUser.url('check-open-store-user/', 'check-open-store-user'),
]
