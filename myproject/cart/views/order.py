from base_class.views import FormView
from base_class.views import ClassView
from cart.models import Booking, BookingItems
from cart.forms import CheckoutForm


class CheckOutFormView(FormView):
    form_class = CheckoutForm

    def save(self, form):
        self.new_render(self.request)

    def new_render(self, request):
        cart = Booking.get_cart()
        if not cart.total_price:
            self.add('error', False)
            self.add('message', 'Your Cart is empty..!!')

        form = self.form_class(request.POST)

        if form.is_valid():
            student_name = form.cleaned_data.get('student_name')
            mobile_number = form.cleaned_data.get('mobile_number')
            email_address = form.cleaned_data.get('email_address')
            admission_number = form.cleaned_data.get('admission_number')
            branch = form.cleaned_data.get('branch')

            cart.student_name = student_name
            cart.mobile_number = mobile_number
            cart.email_address = email_address
            cart.admission_number = admission_number
            cart.branch = branch
            cart.is_mail_send = True
            cart.save()
            form.send_mail(cart)

            self.add('error', False)
            self.add('message', 'Added successfully')
            self.add('cart', cart.id)

        else:
            self.add('error', True)


class CheckOutAPIDetails(ClassView):

    def process(self, request):
        instance = request.POST.get('id')

        try:
            cart = Booking.objects.get(pk=instance)
        except Exception as e:
            self.add('error', True)
            self.add('exception', str(e))
            self.add('message', 'Something went wrong..!!')
        else:
            if not cart.total_price:
                self.add('error', False)
                self.add('message', 'Your Cart is empty..!!')

            if cart.is_mail_send:
                self.add('message', 'Your order under processing. Please try after sometime')

            data = BookingItems.objects.filter(booking_id=cart.id)

            cart_data = {
                "id": cart.id,
                "booking_id": cart.booking_id,
                "total_price": cart.total_price,
                "student_name": cart.student_name,
                "mobile_number": cart.mobile_number,
                "email_address": cart.email_address,
                "admission_number": cart.admission_number,
                "branch": cart.branch,
            }

            items = []
            for i in data:
                it = {
                    "id": i.id,
                    "booking": i.booking.id,
                    "item": i.item.id,
                    "item_name": i.item.name,
                    "image": i.item.image.url,
                    "quantity": i.quantity,
                    "unit_price": i.unit_price,
                    "total_price": i.total_price,
                }
                items.append(it)

            self.add('cart', cart_data)
            self.add('items', items)



