from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.blog.sitemaps import CategorySitemap, PostSitemap

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('', include('apps.blog.urls', namespace='blog')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('api/', include('apps.api.urls', namespace='api')),
    path('markdownx/', include('markdownx.urls')),
    path('admin/', admin.site.urls),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots_txt',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
