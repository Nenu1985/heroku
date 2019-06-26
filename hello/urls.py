from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'hello'

urlpatterns = [
    # post views
    path('success_message/', views.success_message, name='success'),
    path('error_message/', views.error_message, name='error'),
    path("db/", views.db, name="db"),
]
