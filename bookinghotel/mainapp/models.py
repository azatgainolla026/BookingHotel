from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', ]


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotels/')

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class Room(models.Model):
    class RoomChoices(models.TextChoices):
        SINGLE = 'Single'
        DOUBLE = 'Double'
        LARGE = 'Large'
        VIP = 'Vip'

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100, choices=RoomChoices.choices)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='rooms/',null=True,blank=True)


    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"

    @property
    def is_available(self):
        return self.stock > 0


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class BookingStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_positive(self):
        return self.rating >= 4
