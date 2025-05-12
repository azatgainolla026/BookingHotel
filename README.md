 Hotel Booking API
                                    Each endpoint and method must have unittest


A fully-featured hotel booking system built with Django and Django REST Framework.

 Features

- User registration and authentication (JWT)
- Full CRUD for Cities, Hotels, Rooms, Reviews, and Bookings
- User profile with booking and review history
- Room reservation with asynchronous confirmation (Celery)
- Hotel list caching (Redis)
- Request throttling for users and guests
- Profiling with Django Silk
- Swagger/OpenAPI auto-generated API docs
- Fully containerized with Docker Compose

 Tech Stack

- Python 3.11
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- MinIO / S3-compatible object storage
- Docker & Docker Compose
- Nginx
- drf-spectacular (Swagger)
- django-silk (Profiling)
- SimpleJWT for Authentication

 API Endpoints Overview

 Authentication
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/token/refresh/`

 Cities
- `GET /api/cities/`
- `POST /api/cities/`
- `GET /api/cities/{id}/`
- `PUT /api/cities/{id}/`
- `DELETE /api/cities/{id}/`
- `GET /api/cities/{city_id}/hotels/`

 Hotels
- `GET /api/hotels/`
- `POST /api/hotels/`
- `GET /api/hotels/{id}/`
- `PUT /api/hotels/{id}/`
- `PATCH /api/hotels/{id}/`
- `DELETE /api/hotels/{id}/`
- `GET /api/hotels/{hotel_id}/rooms/`
- `GET /api/hotels/{hotel_id}/reviews/`
- `POST /api/hotels/{hotel_id}/reviews/`
- `DELETE /api/hotels/{hotel_id}/reviews/{id}/`

Rooms
- `GET /api/rooms/`
- `POST /api/rooms/`
- `GET /api/rooms/{id}/`
- `PUT /api/rooms/{id}/`
- `PATCH /api/rooms/{id}/`
- `DELETE /api/rooms/{id}/`
- `POST /api/rooms/{room_id}/reserve/`

 User
- `GET /api/user/profile/`
- `GET /api/user/reserves/`
- `GET /api/user/reserves/{id}/`
- `PATCH /api/user/reserves/{booking_id}/cancel/`
- `GET /api/user/reviews/`
- `GET /api/user/reviews/{id}/`
- `DELETE /api/user/reviews/{id}/`

 Testing

All endpoints and methods are covered with unit tests using Django’s `TestCase` and `APITestCase`.

 Throttling

- Anonymous users: 10 requests per minute  
- Authenticated users: 100 requests per minute

 API Docs

Swagger UI is available at:

Authentication Tests (AuthTests):

Registering a new user and handling existing emails or usernames.

Login functionality, including testing invalid credentials.

Token refresh functionality.

City API Tests (CityAPITestCase):

Listing cities, creating new cities (restricted to admins), updating and deleting cities by admins.

Accessing hotel data related to a city.

Hotel API Tests (HotelAPITestCase):

Listing hotels, creating, updating, and deleting hotels (admin-only for creation, update, and delete).

Retrieving hotel details and reviewing hotels.

Review API Tests (ReviewAPITestCase):

Admin can delete reviews.

Regular users can only delete their own reviews or list them.

Users can retrieve their reviews and their details.

Room API Tests (RoomAPITestCase):

Admin users can create, update, delete rooms.

Regular users cannot create or delete rooms, but they can reserve them if available.

Users can get the list of rooms, details of rooms, and reserve them.

User Profile and Reservation Tests (UserAPITestCase):

Users can retrieve their profile and reservation details.

Users can create and cancel bookings.

Testing the functionality for managing user reserves.

Observations:
The code ensures that permissions are handled correctly (e.g., only admins can create or update cities and hotels).

It also verifies that users can only manage their own reviews and reservations.

For each functionality, appropriate tests are provided (e.g., checking forbidden access for unauthorized users).

Test cases use realistic scenarios like creating a booking, updating room information, and handling reviews.

                                                              SWAGER DOC

Authentication Endpoints:
POST /api/auth/login/ - Used for user login.

POST /api/auth/register/ - Allows a user to register.

POST /api/auth/token/refresh/ - Refreshes an authentication token.

Cities:
GET /api/cities/ - Lists all cities.

POST /api/cities/ - Creates a new city.

GET /api/cities/{city_id}/hotels/ - Lists hotels in a specific city.

GET /api/cities/{id}/ - Retrieves a specific city by ID.

PUT /api/cities/{id}/ - Updates a city.

DELETE /api/cities/{id}/ - Deletes a city.

Hotels:
GET /api/hotels/ - Lists all hotels.

POST /api/hotels/ - Creates a new hotel.

GET /api/hotels/{hotel_id}/reviews/ - Retrieves reviews for a hotel.

POST /api/hotels/{hotel_id}/reviews/ - Adds a review to a hotel.

DELETE /api/hotels/{hotel_id}/reviews/{id}/ - Deletes a specific hotel review.

GET /api/hotels/{hotel_id}/rooms/ - Lists rooms in a specific hotel.

GET /api/hotels/{id}/ - Retrieves a specific hotel by ID.

PUT /api/hotels/{id}/ - Updates a hotel.

PATCH /api/hotels/{id}/ - Partially updates a hotel.

DELETE /api/hotels/{id}/ - Deletes a hotel.

Rooms:
GET /api/rooms/ - Lists all rooms.

POST /api/rooms/ - Creates a new room.

GET /api/rooms/{id}/ - Retrieves a specific room.

PUT /api/rooms/{id}/ - Updates a room.

PATCH /api/rooms/{id}/ - Partially updates a room.

DELETE /api/rooms/{id}/ - Deletes a room.

POST /api/rooms/{room_id}/reserve/ - Reserves a room.

User:
GET /api/user/profile/ - Retrieves the user profile.

GET /api/user/reserves/ - Lists the user's reservations.

PATCH /api/user/reserves/{booking_id}/cancel/ - Cancels a specific reservation.

GET /api/user/reserves/{id}/ - Retrieves a specific reservation.

GET /api/user/reviews/ - Lists the user's reviews.

GET /api/user/reviews/{id}/ - Retrieves a specific review by the user.

DELETE /api/user/reviews/{id}/ - Deletes a review by the user.

Schemas:
The API has several schemas for data structure, including:

Booking - Defines a booking object.

City - Defines a city object.

Hotel - Defines a hotel object.

PatchedHotel - Defines a partially updated hotel object.

PatchedRoom - Defines a partially updated room object.

Register - Defines the user registration schema.

Review - Defines the hotel review schema.

Room - Defines a room object.

RoomReserve - Defines a room reservation object.

RoomTypeEnum - Defines possible room types.

StatusEnum - Defines possible statuses (e.g., reservation status).

TokenObtainPair - Defines the schema for obtaining tokens.

TokenRefresh - Defines the schema for refreshing tokens.

User - Defines the user object schema.
    
              
                      SILK
Install
pip install django-silk
  INSTALLED_APPS
INSTALLED_APPS = [
'silk',
]
  urls.py
path('silk/', include('silk.urls', namespace='silk')),


  Install Django REST Framework
pip install djangorestframework

  Configure Throttling in settings.py

  REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  
        'rest_framework.throttling.UserRateThrottle',  
    ,
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/day',   # Allow 5 requests per day for anonymous users
        'user': '1000/day', # Allow 1000 requests per day for authenticated users
    }
}
   Customize Throttling 
   If you want to create a custom throttling class, you can subclass BaseThrottle and implement your own throttling logic.
from rest_framework.throttling import BaseThrottle
import time

class CustomRateThrottle(BaseThrottle):
    def __init__(self):
        self.history = []
        self.rate = 5  # Number of requests allowed
        self.duration = 60 * 60  # 1 hour in seconds

    def allow_request(self, request, view):
        # Check how many requests have been made in the last `duration` seconds
        self.history = [timestamp for timestamp in self.history if timestamp > time.time() - self.duration]
        
        if len(self.history) < self.rate:
            # Allow the request if the rate hasn't been exceeded
            self.history.append(time.time())
            return True
        return False

  Then, add your custom throttle class to the DEFAULT_THROTTLE_CLASSES in your settings.py:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ,
    'DEFAULT_THROTTLE_RATES': {
        'anon': '15/minute',
        'user': '100/minute',
        'burst': '10/minute',
        'sustained': '100/hour'
    }
}
                Fully deployable with docker-compose.yml
1. Using a requirements.txt File for Dependencies:
You're copying the requirements.txt file and installing dependencies. This is a good practice, but make sure that your requirements.txt includes everything required for production, such as gunicorn, psycopg2 (or asyncpg for async database connections), and any other dependencies that your project uses.

2. Static File Collection:
The command python manage.py collectstatic --noinput runs during the Docker image build to gather static files for production. Ensure that you have configured Django to use a proper storage backend for static files (e.g., django-storages with S3 or MinIO). If you're serving static files with Nginx, this will be sufficient.

3. Database Migrations:
Consider adding a RUN command to run migrations during the Docker image build or entrypoint, ensuring the database is up-to-date before starting the app.

You can modify your Dockerfile to automatically run migrations when the container starts:

dockerfile
Copy
Edit

docker-compose.yml file defines several key services and technologies used in your setup:

PostgreSQL (db): A relational database used to store your app's data. It's configured using environment variables from a .env file, and its data is persisted in a volume (pg_data).
services:
  db:
    image: postgres:15
    volumes:
      - pg_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    env_file:
      - .env
    ports:
      - "5432:5432"

Redis (redis): A caching system used for improving performance and handling asynchronous tasks with Celery. It listens on port 6379 and is linked to other services like Celery.
 redis:
    image: redis:latest
    ports:
      - "6379:6379"
Django (web): The main web application built with Django. It is run using Gunicorn, a WSGI server, in a production-ready setup. The app is exposed on port 8000.
web:
    build: .
    restart: always
    container_name: web-back
    volumes:
      - .:/app
      - static_volume:/app/static
    expose:
      - "8000"
    ports:
      - "8000:8000"
    depends_on:
      - db
      - minio
      - redis
    env_file:
      - .env
    environment:
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}

Celery (celery): A distributed task queue that is used for running asynchronous background tasks, such as sending emails or processing images. It connects to Redis as the broker for task queues.
celery:
    build: .
    command: celery -A bookinghotel worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis
      - db
    env_file:
      - .env
Nginx (nginx): A reverse proxy and web server that sits in front of the Django application. It handles HTTP requests and serves static files. It’s configured to use a custom nginx.conf file and is exposed on port 80.

nginx:
    image: nginx:latest
    ports:
      - "80:80"
    depends_on:
      - web
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/static
PgAdmin (pgadmin): A web-based interface for managing PostgreSQL databases. It allows for easier database administration and can be accessed on port 5050.
 pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports:
      - "5050:80"
    depends_on:
      - db
MinIO (minio): An object storage service that is compatible with Amazon S3. It provides scalable, high-performance storage for files and objects. It is exposed on ports 9000 for the API and 9001 for the management console.
minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    environment:
      MINIO_ROOT_USER: ${MINIO_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY}

Volumes: Volumes are defined for persistent data storage:

pg_data: for PostgreSQL data.

static_volume: for static files served by Django and Nginx.

minio_data: for MinIO's data storage.
