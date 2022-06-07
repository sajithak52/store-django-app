from base_class.views import ModelListView
from base_class.views import FormView
from base_class.views import ClassView

from cart.models import Booking, BookingItems

from cart.forms import PurchaseForm


class AllBookingList(ModelListView):
    has_pagination = False
    fields = []

    def get_query(self):
        booking_status = self.request.GET.get('status')

        query = Booking.objects.all()

        if booking_status == 'Packed':
            return query.filter(is_purchased=False).order_by('-id')

        elif booking_status == 'Purchased':
            return query.filter(is_purchased=True).order_by('-id')

        else:
            return query.order_by('-id')

    def to_json(self, record):
        data = {
            'id': record.id,
            'booking_id': record.booking_id,
            'student_name': record.student_name if record.student_name else '',
            'created_at': record.created_at.strftime("%d %B, %Y") if record.created_at else '',
            'email': record.email_address,
            'mobile_number': record.mobile_number,
            'admission_number': record.admission_number,
            'branch': record.branch,
            'total_price': record.total_price
        }
        return data


class CartItemsList(ModelListView):
    fields = []
    has_pagination = False

    def get_query(self):
        cart = self.request.GET.get('id')

        if cart not in ['', ' ', None, 'undefined', 'null']:
            query = BookingItems.objects.filter(booking_id=cart)
            return query

        else:
            return []

    def to_json(self, record):
        data = {
            'id': record.id,
            'booking': record.booking.id,
            'item': record.item.id,
            'item_name': record.item.name,
            'name': record.name,
            'quantity': record.quantity,
            'price': record.unit_price,
            'total': record.total_price
        }
        return data


class GetPurchaseDetails(ClassView):
    form_class = PurchaseForm

    def process(self, request):

        form = self.form_class(request.POST)

        if not form.is_valid():
            self.add('error', True)
            self.add('success', False)
            self.add('message', 'There is not booking details..!!')
            return self

        instance = form.cleaned_data.get('booking')

        details = {
            'created_at': instance.created_at.strftime("%d %b, %Y"),
            'completed_at': instance.completed_at.strftime("%d %b, %Y") if instance.completed_at else '',
            'booking_id': instance.booking_id,
            'total_price': instance.total_price,
            'student_name': instance.student_name,
            'mobile_number': instance.mobile_number,
            'email_address': instance.email_address,
            'admission_number': instance.admission_number,
            'branch': instance.branch,
            'is_purchased': instance.is_purchased,
            'is_mail_send': instance.is_mail_send,
        }

        items = BookingItems.objects.filter(booking_id=instance.pk)

        item_details = [{
            'item': i.item.id,
            'item_name': i.item.name,
            'quantity': i.quantity,
            'unit_price': i.unit_price,
            'total_price': i.total_price,
        } for i in items]

        details["items"] = item_details

        self.add('error', False)
        self.add('success', True)
        self.add('data', details)


class PurchaseOrder(FormView):
    form_class = PurchaseForm

    def save(self, form):
        order = form.cleaned_data.get('booking')
        print("booking : ", order)
        print("order id : ", order.booking_id)

        order.is_purchased = True
        order.save()



