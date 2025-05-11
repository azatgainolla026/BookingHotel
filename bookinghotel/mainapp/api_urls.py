from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api_views import CityViewSet, HotelViewSet, RoomViewSet, HotelListByCityAPIView, RoomListByHotelAPIView, \
    ReviewListCreateAPIView, ReviewDeleteAPIView, UserProfileAPIView, UserReviewListAPIView, UserReviewDeleteAPIView, \
    RoomReserveAPIView, UserBookingListAPIView, CancelBookingAPIView, UserBookingDetailAPIView, RegisterAPIView

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    # api
    path('', include(router.urls)),
    path('cities/<int:city_id>/hotels/', HotelListByCityAPIView.as_view(), name='hotels-by-city'),
    path('hotels/<int:hotel_id>/rooms/', RoomListByHotelAPIView.as_view(), name='rooms-by-hotel'),
    path('hotels/<int:hotel_id>/reviews/', ReviewListCreateAPIView.as_view(), name='hotel-reviews-list-create'),
    path('hotels/<int:hotel_id>/reviews/<int:pk>/', ReviewDeleteAPIView.as_view(), name='review-delete'),
    path('user/profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('user/reviews/', UserReviewListAPIView.as_view(), name='user-reviews'),
    path('user/reviews/<int:pk>/', UserReviewDeleteAPIView.as_view(), name='user-review-delete'),
    path('rooms/<int:room_id>/reserve/', RoomReserveAPIView.as_view(), name='room-reserve'),
    path('user/reserves/', UserBookingListAPIView.as_view(), name='user-reserves'),
    path('user/reserves/<int:pk>/', UserBookingDetailAPIView.as_view(), name='user-booking-detail'),
    path('user/reserves/<int:booking_id>/cancel/', CancelBookingAPIView.as_view(), name='cancel-booking'),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
