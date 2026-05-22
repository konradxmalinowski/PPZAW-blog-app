from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.timezone import now

from apps.blog.models import Category, Post


class PostSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Post.published.select_related('author', 'category').all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()

    def priority(self, obj):
        age_days = (now() - obj.publish).days
        if age_days < 30:
            return 0.9
        if age_days < 180:
            return 0.7
        return 0.5

    def changefreq(self, obj):
        age_days = (now() - obj.publish).days
        if age_days < 30:
            return 'daily'
        if age_days < 180:
            return 'weekly'
        return 'monthly'


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return ['blog:post_list', 'blog:post_search']

    def location(self, item):
        return reverse(item)
