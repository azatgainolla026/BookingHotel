from django.shortcuts import render
from django.contrib.auth.decorators import login_required
def main_page(request):
    return render(request, 'mainapp/main_page.html')
def about_page(request):
    return render(request, 'mainapp/about.html')
def login_page(request):
    return render(request, 'mainapp/login.html')
def register_page(request):
    return render(request, 'mainapp/register.html')
@login_required(login_url='/login/')
def profile_view(request):
    return render(request, 'mainapp/profile.html')
@login_required
def reserves_page(request):
    return render(request, 'mainapp/reserves.html')
