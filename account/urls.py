from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

urlpatterns = [
    # post views
    path('login/', views.user_login, name='login'),
    path('login-django/', auth_views.LoginView.as_view(template_name='account/registration/login-django.html'),
         name='login-django'),
    path('logout-django/', auth_views.LogoutView.as_view(template_name='account/registration/log_out.html'),
         name='logout-django'),
    path('', views.dashboard, name='dashboard'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='account/registration/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeView.as_view(template_name='account/registration/password_change_done.html'),
         name='password_change_done'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/', login_required(views.UserListView.as_view()), name='user-list'),
    path('users/follow/', views.UserFollowView.as_view(), name='user-follow'),
    path('users/<int:pk>/', login_required(views.UserDetailView.as_view()), name='user-detail'),
    path('users/<username>/', login_required(views.UserDetailView.as_view()), name='user_detail'),
    # path('users/', login_required(views.UserListView.as_view()), name='user_list'),
    # path('users/follow/', views.UserFollowView.as_view(), name='user_follow'),
    # path('users_c/<username>/', , name='user_detail_c'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
