from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('sales/', views.sales_page, name='sale'),
    path('sales/add/', views.add_sales_record,
         name='add sales'),
    path('sale/details/<int:pk>/', views.SaleDetailView.as_view(),
         name='single sale record'),
    path('sale/delete/<int:pk>/', views.delete_sale_record,
         name='delete single sale'),
    path('products/', views.product_page, name='product'),
    path('product/add/', views.add_product_record,
         name='add product'),
    path('product/details/<int:pk>/', views.ProductDetailView.as_view(),
         name='product details'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('change_password/', views.ChangePassword.as_view(),
         name='change password'),
    path('password_reset', views.PasswordReset.as_view,
         name='reset password'),
    path('profile/', views.profile, name='profile'),
    path('view_profile/<int:pk>/', views.member_profile,
         name='member profile'),
    path('update_profile/<int:pk>/', views.user_update,
         name='update user'),
    path('add_member/', views.add_user, name='add member')


]
