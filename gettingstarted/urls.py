from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
# from django.contrib.sitemaps.views import sitemap
# from blog.sitemap import PostSitemap
#
# sitemaps = {
#     'posts': PostSitemap,
# }

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path('hello/', include('hello.urls', namespace='hello')),
    path("admin/", admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('collage/', include('collage.urls', namespace='collage')),
    path('pizzashop/', include('pizzashopapp.urls', namespace='pizzapp')),
    path('celery-progress/', include('celery_pb.urls')),  # the endpoint is configurable
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('account/', include('account.urls', namespace='account')),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    #      name='django.contrib.sitemaps.views.sitemap')

    # path('progressbarupload/', include('progressbarupload.urls')),
# reset password urls
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
         auth_views.PasswordResetCompleteView.as_view(template_name='account/registration/password_reset_complete.html'),
         name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
