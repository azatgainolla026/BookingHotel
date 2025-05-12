from celery import shared_task
from .models import Booking

@shared_task
def confirm_booking(booking_id):
    try:
        booking = Booking.objects.select_related('room').get(id=booking_id)
        if booking.status == Booking.BookingStatus.PENDING and booking.room.stock > 0:
            booking.status = Booking.BookingStatus.CONFIRMED
            booking.room.stock -= 1
            booking.room.save()
            booking.save()
            return f"Booking {booking_id} confirmed."
        return f"Booking {booking_id} skipped due to invalid status or no stock."
    except Booking.DoesNotExist:
        return f"Booking {booking_id} does not exist."