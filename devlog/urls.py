from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.blog.sitemaps import CategorySitemap, PostSitemap, StaticSitemap


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['SITE_URL'] = settings.SITE_URL
        ctx['DEBUG'] = settings.DEBUG
        return ctx


sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'static': StaticSitemap,
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
        RobotsTxtView.as_view(),
        name='robots_txt',
    ),
]

handler429 = 'devlog.views.handler429'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass
