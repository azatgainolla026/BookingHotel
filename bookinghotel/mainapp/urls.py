from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # auth pages
    path('login/', TemplateView.as_view(template_name='mainapp/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='mainapp/register.html'), name='register'),

    # main pages
    path('hotels/', TemplateView.as_view(template_name='mainapp/hotels.html'), name='hotels'),
    path('', TemplateView.as_view(template_name='mainapp/main.html'), name='main'),
    path('profile/', TemplateView.as_view(template_name='mainapp/profile.html'), name='profile'),

    path('hotels/<int:id>/', TemplateView.as_view(template_name='mainapp/hotel-detail.html'), name='hotel_detail'),
    path('rooms/<int:id>/', TemplateView.as_view(template_name='mainapp/room-detail.html'), name='room_detail')

]
