from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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
    path("my-page/", hello.views.my_page, name='my_page'),
    path("db/", hello.views.db, name="db"),
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
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
