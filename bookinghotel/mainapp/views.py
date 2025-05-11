from django.shortcuts import render

def main_page(request):
    return render(request, 'mainapp/main_page.html')
def about_page(request):
    return render(request, 'mainapp/about.html')
def login_page(request):
    return render(request, 'mainapp/login.html')
def register_page(request):
    return render(request, 'mainapp/register.html')
