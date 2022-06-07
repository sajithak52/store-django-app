from django.contrib import admin
from .models import Booking
from .models import BookingItems


admin.site.register(Booking)
admin.site.register(BookingItems)


