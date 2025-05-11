from django.db.models import Avg
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import City, Hotel, Room, Review, Booking, User
from .serializers import CitySerializer, HotelSerializer, RoomSerializer, ReviewSerializer, UserSerializer, \
    BookingSerializer, RoomReserveSerializer, RegisterSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class HotelListByCityAPIView(generics.ListAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self):
        return Hotel.objects.filter(city_id=self.kwargs['city_id'])


class RoomListByHotelAPIView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Room.objects.filter(hotel_id=hotel_id)


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Review.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        hotel_id = self.kwargs['hotel_id']
        hotel = Hotel.objects.get(id=hotel_id)
        serializer.save(user=self.request.user, hotel=hotel)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        reviews = queryset.all()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        serializer = self.get_serializer(reviews, many=True)

        return Response({
            'average_rating': average_rating,
            'reviews': serializer.data
        })


class ReviewDeleteAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAdminUser]


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class UserReviewDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        instance.delete()


class RoomReserveAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomReserveSerializer

    @extend_schema(
        request=RoomReserveSerializer,
        responses=BookingSerializer,
        description="Reserve a room if it is available. Returns created booking."
    )
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)

        if not room.is_available:
            return Response(
                {"detail": "This room is not available for reservation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']

        booking = Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            status=Booking.BookingStatus.PENDING
        )

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class UserBookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')


class UserBookingDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class CancelBookingAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=BookingSerializer)
    def patch(self, request, booking_id):
        # Получаем бронирование для текущего пользователя
        booking = get_object_or_404(Booking, id=booking_id)

        # Проверяем, что это бронирование текущего пользователя
        if booking.user != request.user:
            return Response(
                {"detail": "You cannot cancel someone else's booking."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Если бронирование уже отменено
        if booking.status == Booking.BookingStatus.CANCELLED:
            return Response(
                {"detail": "Booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Обновляем складской запас, если бронирование было подтверждено
        if booking.status == Booking.BookingStatus.CONFIRMED:
            booking.room.stock += 1
            booking.room.save()

        # Меняем статус бронирования на отменённый
        booking.status = Booking.BookingStatus.CANCELLED
        booking.save()

        return Response(
            {"detail": "Booking cancelled successfully."},
            status=status.HTTP_200_OK
        )



class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
