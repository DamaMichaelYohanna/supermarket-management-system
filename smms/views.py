from django.shortcuts import render
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView, PasswordResetView)
from django.contrib.auth.decorators import login_required

from . import models

# Create your views here.


class Login(LoginView):
    """class base login view"""
    template_name = 'account/login.html'


class Logout(LogoutView):
    """class base logout view"""
    template_name = 'account/logout.html'


class ChangePassword(PasswordChangeView):
    """class based view for changing password"""
    template_name = 'account/password_change.html'
    success_url = '/profile/'

    def get_context_data(self, **kwargs):
        kwargs['section'] = 'Profile'
        return super().get_context_data(**kwargs)


class PasswordReset(PasswordResetView):
    """class base view for resetting user password"""
    template_name = 'account/password_reset.html'


def profile(request):
    user_id = request.user.id
    user_profile = models.Profile.objects.get(user=user_id)
    all_user = models.Profile.objects.all()
    context = {'profile': user_profile, 'all_user': all_user}
    return render(request, 'account/profile.html', context)


@login_required()
def homepage(request):
    """home page"""
    total_product = models.TotalProduct.objects.all().count()
    sales = models.Sale.objects.all().count()
    product = models.Product.objects.all().count()
    context = {'section': 'Dashboard', 'total': total_product, 'sales': sales,
               'product': product}
    return render(request, 'home.html', context)
