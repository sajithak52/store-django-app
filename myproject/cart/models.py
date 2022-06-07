from django.db import models
from .utils import generate_booking_id
from base_class.middlewares.request import CurrentRequestMiddleware
from store_management.models import Product


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, db_index=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    booking_id = models.CharField(max_length=256)

    total_price = models.IntegerField()

    student_name = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=64, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    admission_number = models.CharField(max_length=256, blank=True, null=True)
    branch = models.CharField(max_length=200, blank=True, null=True)

    is_purchased = models.BooleanField(default=False, db_index=True)
    is_mail_send = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.admission_number} - {self.student_name}"

    @classmethod
    def get_cart(cls):
        # request = get_current_request()
        request = CurrentRequestMiddleware.get_request()

        session_key = request.session.session_key
        if not request.session.exists(session_key):
            request.session.create()
        session_key = request.session.session_key

        try:
            return Booking.objects.get(session_key=session_key, is_mail_send=False, is_purchased=False)
        except Booking.DoesNotExist:
            return Booking.objects.create(session_key=session_key, total_price=0)

    def update_total(self):
        items = BookingItems.objects.filter(booking=self)
        total = 0
        for item in items:
            total += item.total_price

        self.total_price = total
        self.save()

    def add_item(self, product, quantity, booking_item=None):

        if booking_item is None:
            cart_item, created = BookingItems.objects.get_or_create(
                item_id=product.id, booking=self,
                unit_price=product.selling_price,
            )

            if not created:
                cart_item.quantity += quantity
                if quantity > 0:
                    product.stock -= quantity
                    product.save()
                else:
                    product.stock -= quantity
                    product.save()
            else:
                product.stock -= 1
                product.save()

            total = cart_item.unit_price * cart_item.quantity
            cart_item.total_price = total
            cart_item.save()

            if cart_item.quantity <= 0:
                cart_item.delete()
        else:
            total = product.selling_price * quantity

            cart_item = BookingItems.objects.get(pk=booking_item)
            actual_quantity = cart_item.quantity + quantity
            cart_item.quantity = actual_quantity
            cart_item.total_price = total
            cart_item.save()
            if quantity > 0:
                product.stock += quantity
                product.save()
            else:
                product.stock -= quantity
                product.save()

    @classmethod
    def add_to_current_cart(cls, product, quantity, booking_item=None):
        cart = cls.get_cart()
        cart.add_item(product, quantity, booking_item)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.booking_id:
            self.booking_id = generate_booking_id()
        op = models.Model.save(self, force_insert, force_update, using, update_fields)
        return op


class BookingItems(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    unit_price = models.IntegerField(default=0, blank=True, null=True)
    total_price = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.item.name} * {self.quantity}"

    def save(self, *args, **kwargs):
        super(BookingItems, self).save()
        self.booking.update_total()

    def delete(self, using=None, keep_parents=False):
        op = models.Model.delete(self, using)
        self.booking.update_total()




