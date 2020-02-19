from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == 'POST':
        print('it a post method', request.POST.get('username'))
    else:
        print('not a post request')
    return render(request, 'account/login.html')


class Login(LoginView):
    """class base login view"""
    template_name = 'account/login.html'


class Logout(LogoutView):
    """class base logout view"""
    template_name = 'account/logout.html'


def profile(request):
    return render(request, 'account/profile.html')


@login_required()
def homepage(request):
    """home page"""
    return render(request, 'home.html')
