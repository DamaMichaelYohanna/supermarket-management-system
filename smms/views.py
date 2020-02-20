from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from . import models


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
    total_product = models.TotalProduct.objects.all().count()
    sales = models.Sale.objects.all().count()
    product = models.Product.objects.all().count()
    context = {'section': 'Dashboard', 'total': total_product, 'sales': sales,
               'product': product}
    return render(request, 'home.html', context)
