import random


def generate_booking_id():

    booking_id = 'ORD'

    first_ = random.randint(100, 999)
    second_ = random.randint(100, 999)

    booking_id = booking_id + str(first_) + str(second_)

    from .models import Booking
    is_exist = Booking.objects.filter(booking_id=booking_id).exists()

    if is_exist:
        booking_id = generate_booking_id()
        return booking_id

    return booking_id

