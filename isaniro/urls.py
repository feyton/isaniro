
from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

sitemaps = {
    "posts": PostSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include(("blog.urls", 'blog'), namespace='blog')),
    path('user/', include("user.urls")),
    path("", include("index.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
