from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # post views
    path('login/', views.user_login, name='login'),
    path('login-django/', auth_views.LoginView.as_view(template_name='account/registration/login.html'),
         name='login-django'),
    path('logout-django/', auth_views.LogoutView.as_view(template_name='account/registration/log_out.html'),
         name = 'logout-django'),
    path('', views.dashboard, name='dashboard'),
]