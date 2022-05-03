from .views import AllBookingList
from .views import GetPurchaseDetails
from .views import PurchaseOrder

from .views import AddToCartJSONView
from .views import RemoveCartItemAPIJSONView
from .views import CartItemsList

from .views import CheckOutFormView
from .views import CheckOutAPIDetails


urlpatterns = [
    AllBookingList.url('all-bookings/', 'all-bookings'),
    GetPurchaseDetails.url('get-purchase-details/', 'get-purchase-details'),
    PurchaseOrder.url('purchase-order/', 'purchase-order'),

    CartItemsList.url('cart-item-info/', 'cart-item-info'),

    AddToCartJSONView.url('add-or-reduce-cart/', 'add-or-reduce-cart'),
    RemoveCartItemAPIJSONView.url('remove-cart/', 'remove-cart'),

    CheckOutFormView.url('check-out-form/', 'check-out-form'),
    CheckOutAPIDetails.url('check-out/', 'check-out'),

]
