from . import views
from django.urls import path

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('about/', views.about_page, name='about_page'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('profile/', views.profile_view, name='profile'),
    path('reserves/', views.reserves_page, name='reserves'),
]