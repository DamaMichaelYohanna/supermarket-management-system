from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('change_password/', views.ChangePassword.as_view(),
         name='change password'),
    path('profile/', views.profile, name='profile'),
]
