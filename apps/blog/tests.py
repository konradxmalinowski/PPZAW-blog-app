from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import Category, Post
from apps.blog.seo_context import seo_defaults


class MetaDescriptionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user('seoauthor', password='pw12345!')

    def _post(self, **kwargs):
        defaults = dict(
            title='SEO Post',
            slug='seo-post',
            author=self.author,
            body='',
            publish=timezone.now(),
            status='published',
        )
        defaults.update(kwargs)
        return Post.objects.create(**defaults)

    def test_custom_meta_description_wins(self):
        post = self._post(meta_description='Custom meta', excerpt='Excerpt text', body='Body text')
        self.assertEqual(post.get_meta_description(), 'Custom meta')

    def test_excerpt_fallback_when_no_meta(self):
        post = self._post(excerpt='Short excerpt fallback', body='Body text here')
        self.assertEqual(post.get_meta_description(), 'Short excerpt fallback')

    def test_excerpt_truncated_to_160(self):
        long_excerpt = 'x' * 300
        post = self._post(excerpt=long_excerpt)
        self.assertEqual(len(post.get_meta_description()), 160)

    def test_body_fallback_strips_markdown(self):
        post = self._post(body='# Heading **bold** `code` (parens) [link] >quote real content')
        result = post.get_meta_description()
        for ch in '#*`[]()>':
            self.assertNotIn(ch, result)
        self.assertIn('Heading', result)

    def test_body_fallback_truncated_to_160(self):
        post = self._post(body='word ' * 200)
        self.assertLessEqual(len(post.get_meta_description()), 160)


class CanonicalUrlTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user('canon', password='pw12345!')

    def test_auto_canonical_returns_relative_without_request(self):
        post = Post.objects.create(
            title='C', slug='c-post', author=cls_author(self), body='b',
            publish=timezone.now(), status='published',
        )
        self.assertEqual(post.get_canonical_url(), post.get_absolute_url())

    def test_custom_canonical_wins(self):
        post = Post.objects.create(
            title='C2', slug='c2-post', author=self.author, body='b',
            publish=timezone.now(), status='published',
            canonical_url='https://example.com/custom',
        )
        self.assertEqual(post.get_canonical_url(), 'https://example.com/custom')


def cls_author(case):
    return case.author


class SecurityHeadersTests(TestCase):
    def test_security_headers_present(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertEqual(response['Referrer-Policy'], 'strict-origin-when-cross-origin')
        self.assertIn("default-src 'self'", response['Content-Security-Policy'])
        self.assertIn('camera=()', response['Permissions-Policy'])


class RobotsTxtTests(TestCase):
    def test_robots_txt_renders_site_url(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        body = response.content.decode()
        self.assertIn('Disallow: /admin/', body)
        self.assertIn('Disallow: /search/', body)
        self.assertIn('http://127.0.0.1:8000/sitemap.xml', body)


class SitemapTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = User.objects.create_user('sm', password='pw12345!')
        cls.category = Category.objects.create(name='Cat', slug='cat')
        Post.objects.create(
            title='P', slug='p-post', author=author, category=cls.category,
            body='b', publish=timezone.now(), status='published',
        )

    def test_sitemap_includes_static_and_post_urls(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('/p-post/', body)
        self.assertIn('/search/', body)


class SeoContextProcessorTests(TestCase):
    def test_seo_defaults_keys(self):
        ctx = seo_defaults(None)
        for key in ('SITE_NAME', 'SITE_URL', 'SITE_DESCRIPTION', 'SITE_DEFAULT_IMAGE', 'TWITTER_HANDLE'):
            self.assertIn(key, ctx)
        self.assertEqual(ctx['SITE_NAME'], 'DevLog')
