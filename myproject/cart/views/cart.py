from base_class.views import ModelListView
from base_class.views import ClassView

from cart.models import Booking, BookingItems
from cart.forms import AddCartForm
from store_management.models import Product


def validate_data(data, keys):
    if not data:
        return False
    new_data = []
    for i in data:
        new_dict = {}
        for key in keys:
            if key in i:
                new_dict[key] = i[key]
            else:
                return False
        new_data.append(new_dict)
    return new_data


class AddToCartJSONView(ClassView):

    def process(self, request):
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')

        product_query = Product.objects.get(pk=product)

        stock = product_query.stock if product_query.stock else 0

        is_exist = int(stock) - int(quantity)

        if is_exist < 0:
            self.add('error', True)
            self.add('success', False)
            self.add('message', f'{product_query.name} is {product_query.stock} in the stock..')
            return self

        Booking.add_to_current_cart(product_query, int(quantity))

        self.add('error', False)
        self.add('success', True)


class RemoveCartItemAPIJSONView(ClassView):

    def process(self, request):
        item = request.POST.get('id')
        cart_item = BookingItems.objects.get(pk=item)
        quantity = cart_item.quantity
        product = cart_item.item.id
        cart_item.delete()

        product_query = Product.objects.get(pk=product)
        product_query.stock += quantity
        product_query.save()

        cart = Booking.get_cart()
        if not cart.total_price:
            self.add('error', False)
            self.add('message', 'Your Cart is empty..!!')
            return self

        self.add('error', False)
        self.add('message', 'Successfully removed item..!!')


class CartItemsList(ModelListView):
    fields = []
    has_pagination = False

    def get_query(self):
        cart = self.request.GET.get('id')

        if cart not in ['', ' ', None, 'undefined', 'null']:
            query = BookingItems.objects.filter(booking_id=cart)

        else:
            cart = Booking.get_cart()
            query = BookingItems.objects.filter(booking_id=cart)

        return query

    def to_json(self, record):
        data = {
            'id': record.id,
            'booking': record.booking.id,
            'item': record.item.id,
            'item_name': record.item.name,
            'quantity': record.quantity,
            'unit_price': record.unit_price,
            'total_price': record.total_price,
            'loading_plus': False,
            'loading_minus': False
        }
        return data




