from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import City, Hotel, Room, Booking, Review

User = get_user_model()


class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.token_refresh_url = reverse('token_refresh')

        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }

        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('access', response.data['token'])
        self.assertIn('refresh', response.data['token'])

    def test_register_with_existing_email(self):
        response = self.client.post(self.register_url, {
            'username': 'anotheruser',
            'email': 'test@example.com',
            'password': 'somepassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_username(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',  # already used
            'email': 'another@example.com',
            'password': 'somepassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        refresh_token = login_response.data['refresh']

        refresh_response = self.client.post(self.token_refresh_url, {
            'refresh': refresh_token
        })
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)


class CityAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@example.com'
        )
        self.user = User.objects.create_user(
            username='user', password='userpass', email='user@example.com'
        )
        self.client = APIClient()
        self.city = City.objects.create(name="Paris")

    def test_list_cities(self):
        response = self.client.get('/api/cities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_city_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/cities/', {'name': 'London'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'London')

    def test_create_city_as_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/cities/', {'name': 'Berlin'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_city_detail(self):
        response = self.client.get(f'/api/cities/{self.city.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Paris')

    def test_update_city_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f'/api/cities/{self.city.id}/', {'name': 'Updated City'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated City')

    def test_delete_city_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/cities/{self.city.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_hotels_by_city(self):
        Hotel.objects.create(name="Grand Hotel", description="Nice", city=self.city, address="123 St")
        response = self.client.get(f'/api/cities/{self.city.id}/hotels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class HotelAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.user = User.objects.create_user(
            username='user',
            password='userpass',
            email='user@example.com'
        )
        self.client = APIClient()
        self.city = City.objects.create(name="Test City")
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="A good place",
            city=self.city,
            address="123 Main Street",
            image=""
        )

    def test_list_hotels(self):
        response = self.client.get('/api/hotels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_hotel_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'New Hotel',
            'description': 'Some description',
            'city_id': self.city.id,
            'address': 'Some address',
            'image': "",
        }
        response = self.client.post('/api/hotels/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hotel_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Hotel',
            'description': 'Some description',
            'city_id': self.city.id,
            'address': 'Some address',
            'image': ''
        }
        response = self.client.post('/api/hotels/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_hotel(self):
        response = self.client.get(f'/api/hotels/{self.hotel.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_hotel_put(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'Updated Hotel',
            'description': 'Updated description',
            'city_id': self.city.id,
            'address': 'Updated address',
            'image': '',
        }
        response = self.client.put(f'/api/hotels/{self.hotel.id}/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, 'Updated Hotel')

    def test_partial_update_hotel_patch(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Partially Updated'}
        response = self.client.patch(f'/api/hotels/{self.hotel.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, 'Partially Updated')

    def test_delete_hotel(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/hotels/{self.hotel.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hotel.objects.filter(id=self.hotel.id).exists())

    def test_get_hotel_reviews(self):
        Review.objects.create(hotel=self.hotel, user=self.user, rating=4, comment="Nice")
        response = self.client.get(f'/api/hotels/{self.hotel.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('reviews', response.data)

    def test_post_hotel_review(self):
        self.client.force_authenticate(user=self.user)
        data = {'rating': 5, 'comment': 'Excellent'}
        response = self.client.post(f'/api/hotels/{self.hotel.id}/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReviewAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.user = User.objects.create_user(
            username='user',
            password='userpass',
            email='user@example.com'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='otherpass',
            email='other@example.com'
        )
        self.city = City.objects.create(name="Test City")
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Nice hotel",
            city=self.city,
            address="123 Main St",
            image=""
        )
        self.review = Review.objects.create(
            user=self.user,
            hotel=self.hotel,
            rating=4,
            comment="Great!",
        )
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_admin_can_delete_review(self):
        self.authenticate(self.admin_user)
        url = f'/api/hotels/{self.hotel.id}/reviews/{self.review.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_regular_user_cannot_delete_review_as_admin(self):
        self.authenticate(self.user)
        url = f'/api/hotels/{self.hotel.id}/reviews/{self.review.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_list_own_reviews(self):
        self.authenticate(self.user)
        url = '/api/user/reviews/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_can_get_own_review_detail(self):
        self.authenticate(self.user)
        url = f'/api/user/reviews/{self.review.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.review.id)

    def test_user_can_delete_own_review(self):
        self.authenticate(self.user)
        url = f'/api/user/reviews/{self.review.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_user_cannot_delete_other_users_review(self):
        self.authenticate(self.other_user)
        url = f'/api/user/reviews/{self.review.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RoomAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.user = User.objects.create_user(
            username='user',
            password='userpass',
            email='user@example.com'
        )
        self.city = City.objects.create(name="Test City")
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Nice hotel",
            city=self.city,
            address="123 Main St",
            image=""
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_type='Single',
            price_per_night=100,
            stock=5,
            image=""
        )
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_admin_can_create_room(self):
        self.authenticate(self.admin_user)
        url = '/api/rooms/'

        data = {
            "hotel_id": self.hotel.id,
            "room_type": "Single",
            "price_per_night": 150,
            "stock": 5,
            "image": ''
        }

        response = self.client.post(url, data, format='multipart')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 2)

    def test_regular_user_cannot_create_room(self):
        self.authenticate(self.user)
        url = '/api/rooms/'
        data = {
            "hotel": self.hotel.id,
            "room_type": "Double",
            "price_per_night": 120,
            "stock": 2,
            "image": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_room(self):
        self.authenticate(self.admin_user)
        url = f'/api/rooms/{self.room.id}/'

        data = {
            "hotel_id": self.hotel.id,
            "room_type": "Single",
            "price_per_night": 120,
            "stock": 10,
            "image": ''
        }

        response = self.client.put(url, data, format='multipart')  # Use 'multipart' for file uploads
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.price_per_night, 120)
        self.assertEqual(self.room.stock, 10)

    def test_regular_user_cannot_update_room(self):
        self.authenticate(self.user)
        url = f'/api/rooms/{self.room.id}/'
        data = {
            "room_type": "Single",
            "price_per_night": 120,
            "stock": 10,
            "image": ""
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_partially_update_room(self):
        self.authenticate(self.admin_user)
        url = f'/api/rooms/{self.room.id}/'
        data = {
            "price_per_night": 110
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.price_per_night, 110)

    def test_regular_user_cannot_partially_update_room(self):
        self.authenticate(self.user)
        url = f'/api/rooms/{self.room.id}/'
        data = {
            "price_per_night": 110
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_room(self):
        self.authenticate(self.admin_user)
        url = f'/api/rooms/{self.room.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Room.objects.filter(id=self.room.id).exists())

    def test_regular_user_cannot_delete_room(self):
        self.authenticate(self.user)
        url = f'/api/rooms/{self.room.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_get_room_list(self):
        self.authenticate(self.user)
        url = '/api/rooms/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_can_get_room_detail(self):
        self.authenticate(self.user)
        url = f'/api/rooms/{self.room.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.room.id)

    def test_user_can_get_rooms_by_hotel(self):
        self.authenticate(self.user)
        url = f'/api/hotels/{self.hotel.id}/rooms/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_can_reserve_room(self):
        self.authenticate(self.user)
        url = f'/api/rooms/{self.room.id}/reserve/'
        data = {
            "check_in": "2025-06-01",
            "check_out": "2025-06-05"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_reserve_unavailable_room(self):
        self.authenticate(self.user)
        self.room.stock = 0
        self.room.save()
        url = f'/api/rooms/{self.room.id}/reserve/'
        data = {
            "check_in": "2025-06-01",
            "check_out": "2025-06-05"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user',
            password='userpass',
            email='user@example.com'
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.city = City.objects.create(name="Test City")
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Nice hotel",
            city=self.city,
            address="123 Main St"
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_type='Single',
            price_per_night=100,
            stock=5,
            image=""
        )
        self.client = self.client_class()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_user_can_get_profile(self):
        self.authenticate(self.user)
        url = '/api/user/profile/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_user_can_get_own_reserves(self):
        self.authenticate(self.user)
        # Creating a booking for the user
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2025-06-01",
            check_out="2025-06-05",
            status=Booking.BookingStatus.PENDING
        )
        url = '/api/user/reserves/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], booking.id)

    def test_user_can_get_booking_details(self):
        self.authenticate(self.user)
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2025-06-01",
            check_out="2025-06-05",
            status=Booking.BookingStatus.PENDING
        )
        url = f'/api/user/reserves/{booking.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], booking.id)

    def test_user_can_cancel_own_booking(self):
        self.authenticate(self.user)
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2025-06-01",
            check_out="2025-06-05",
            status=Booking.BookingStatus.PENDING
        )
        url = f'/api/user/reserves/{booking.id}/cancel/'
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.BookingStatus.CANCELLED)

    def test_user_cannot_cancel_other_user_booking(self):
        self.authenticate(self.user)
        other_user_booking = Booking.objects.create(
            user=self.admin_user,
            room=self.room,
            check_in="2025-06-01",
            check_out="2025-06-05",
            status=Booking.BookingStatus.PENDING
        )
        url = f'/api/user/reserves/{other_user_booking.id}/cancel/'
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
