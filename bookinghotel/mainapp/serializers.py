from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import City, Hotel, Room, Booking, Review

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class HotelSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source='city', write_only=True
    )

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'city', 'city_id', 'address', 'image']


class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    hotel_id = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(), source='hotel', write_only=True
    )
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = ['id', 'hotel', 'hotel_id', 'room_type', 'price_per_night', 'stock', 'is_available']



class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source='room', write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'user_id', 'room', 'room_id',
            'check_in', 'check_out', 'created_at', 'status'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_positive = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at', 'is_positive']
        read_only_fields = ['id', 'user', 'created_at', 'is_positive']




