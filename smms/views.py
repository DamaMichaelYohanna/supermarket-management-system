from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView, PasswordResetView)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import DetailView

from . import models, utils
from . import forms


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


@login_required()
def profile(request):
    user_id = request.user.id
    user_profile = models.Profile.objects.get(user=user_id)
    all_user = models.Profile.objects.exclude(user=user_id)
    context = {'profile': user_profile, 'all_user': all_user, 'section': 'Profile'}
    return render(request, 'account/profile.html', context)


@login_required()
def delete_user(request, pk):
    models.Profile.objects.get(pk=pk).delete()
    messages.success(request, 'Member has been deleted successfully')
    return redirect('/profile/')


@login_required()
def member_profile(request, pk):
    user_profile = models.Profile.objects.get(pk=pk)
    context = {'section': 'Profile', 'user': user_profile}
    return render(request, 'account/member_profile.html', context)


@login_required()
def add_user(request):
    """function for adding new user"""
    if request.method == "POST":
        base_user_form = forms.UserForm(request.POST, instance=User)
        if base_user_form.is_valid():
            user = base_user_form.save()
            return redirect('/profile/')
        else:
            print('form is not valid')
            base_user_form = forms.UserForm(instance=User)
    else:
        base_user_form = forms.UserForm()
        print('it not a post request')

    context = {'user_form': base_user_form}
    return render(request, 'account/add_user.html', context)


# ----------------------------------------------------------------
@login_required()
def user_update(request, pk):
    user_profile = get_object_or_404(models.Profile, pk=pk)
    if request.method == 'POST':
        update_form = forms.UserUpdateForm(request.POST, request.FILES,
                                           instance=user_profile)
        if update_form.is_valid():
            print('form is valid')
            update_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('/profile/')
        else:
            print('form is not valid')
    else:
        print('not a post method')
        update_form = forms.UserUpdateForm(instance=user_profile)
    context = {'form': update_form, 'section': 'Profile'}
    return render(request, 'account/update_profile.html', context)


@login_required()
def homepage(request):
    """home page"""
    utils.investment_pie()
    total_product = models.TotalProduct.objects.all().count()
    sales = models.Sale.objects.all().count()
    product = models.Product.objects.all().count()
    context = {'section': 'Dashboard', 'total': total_product, 'sales': sales,
               'product': product}
    return render(request, 'home.html', context)


# --------------------------------------------------------------------------------------
@login_required()
def sales_page(request):
    """view all the sale."""
    if request.method == 'POST':
        value = request.POST.get('search')
        query_set = models.Sale.objects.filter(name__icontains=value)
        total_price = 0
        total_price = [total_price + x.price for x in query_set]
        total_goods_found = query_set.count()

        context = {'section': 'Sales', 'sales': query_set, 'total_price': total_price,
                   'goods_sold': total_goods_found}
        return render(request, 'sales.html', context)
    else:
        sale_query = models.Sale.objects.all()
        total_price = models.TotalSalesPrice.objects.all()[0]
        total_goods_sold = sale_query.count()
        paginator = Paginator(sale_query, 2)  # 12 sales in each page
        page = request.GET.get('page')
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            page_object = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            page_object = paginator.page(paginator.num_pages)

        context = {'section': 'Sales', 'page_object': page_object,
                   'total_price': total_price, 'goods_sold': total_goods_sold}
        return render(request, 'sales.html', context)


@login_required()
def add_sales_record(request):
    if request.method == 'POST':
        record_form = forms.AddSaleForm(request.POST, request.FILES)
        if record_form.is_valid():
            record_form.save()
            return redirect('/sales/')
        else:
            record_form = forms.AddSaleForm()
    else:
        record_form = forms.AddSaleForm()
    context = {'section': 'Sales', 'form': record_form}
    return render(request, 'add_sales.html', context)


class SaleDetailView(DetailView):
    """class base view for single sale record"""
    context_object_name = 'record'
    template_name = 'single_sale.html'
    model = models.Sale

    def get_context_data(self, **kwargs):
        kwargs['section'] = 'Sales'
        return super().get_context_data(**kwargs)


@login_required()
def delete_sale_record(request, pk):
    """view to delete single sale record"""
    models.Sale.objects.get(pk=pk).delete()
    messages.success(request, 'Sale record deleted successfully')
    return redirect('/sales/')


# --------------------------------------------------------------------------------------------
@login_required()
def product_page(request):
    """view all the product."""
    products = models.Product.objects.all()

    context = {'products': products, 'section': 'Products'}
    return render(request, 'products.html', context)


class ProductDetailView(DetailView):
    """class base view for single product record"""
    context_object_name = 'record'
    template_name = 'single_product.html'
    model = models.Product

    def get_context_data(self, **kwargs):
        kwargs['section'] = 'Product'
        return super().get_context_data(**kwargs)


@login_required()
def delete_product_record(request, pk):
    """view to delete single product record"""
    models.Product.objects.get(pk=pk).delete()
    messages.success(request, 'product deleted successfully')
    return redirect('/products/')


@login_required()
def add_product_record(request):
    if request.method == 'POST':
        record_form = forms.AddProductForm(request.POST, request.FILES)
        if record_form.is_valid():
            record_form.save()
            return redirect('/sales/')
        else:
            record_form = forms.AddProductForm()
    else:
        record_form = forms.AddProductForm()
    context = {'section': 'Products', 'form': record_form}
    return render(request, 'add_product.html', context)
