from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

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
        fields = ['id', 'hotel', 'hotel_id', 'room_type', 'price_per_night', 'stock','image', 'is_available']

    @extend_schema_field(serializers.BooleanField())
    def get_is_available(self, obj):
        return obj.is_available



class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    room = RoomSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'room',
            'check_in',
            'check_out',
            'created_at',
            'status',
            'total_price'
        ]
        read_only_fields = ['id', 'created_at', 'status']

    def get_total_price(self, obj):
        nights = (obj.check_out - obj.check_in).days
        return obj.room.price_per_night * nights

class RoomReserveSerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_positive = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at', 'is_positive']
        read_only_fields = ['id', 'user', 'created_at', 'is_positive']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 'token')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
