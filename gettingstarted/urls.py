from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path('hello/', include('hello.urls', namespace='hello')),
    path("admin/", admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('collage/', include('collage.urls', namespace='collage')),
    path('pizzashop/', include('pizzashopapp.urls', namespace='pizzapp')),
    path('celery-progress/', include('celery_pb.urls')),  # the endpoint is configurable
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('account/', include('account.urls', namespace='account')),
    path('images/', include('images.urls', namespace='images')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('rosetta/', include('rosetta.urls', )),
    path('courses/', include('courses.urls', namespace='courses')),
    path('students/', include('students.urls', namespace='students')),
    path('account/password_reset/',
         auth_views.PasswordResetView.as_view(template_name='account/registration/password_reset_form.html'),
         name='password_reset'),
    path('account/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/registration/password_reset_done.html'),
         name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('account/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path("", hello.views.index, name="index"),
)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
