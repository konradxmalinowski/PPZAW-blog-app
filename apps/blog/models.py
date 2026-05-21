import re

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#7ee787')
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('blog:post_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    body = MarkdownxField()
    excerpt = models.TextField(max_length=500, blank=True)
    cover_image = models.ImageField(upload_to='posts/%Y/%m/', blank=True)
    tags = TaggableManager()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    reading_time = models.PositiveIntegerField(default=0)

    # SEO fields
    meta_description = models.CharField(
        max_length=160, blank=True,
        help_text='Meta description (max 160 chars). Puste = auto z excerpt.'
    )
    meta_keywords = models.CharField(
        max_length=255, blank=True,
        help_text='Słowa kluczowe oddzielone przecinkami.'
    )
    cover_image_alt = models.CharField(
        max_length=125, blank=True,
        help_text='Alt text dla cover image (SEO + dostępność).'
    )
    canonical_url = models.URLField(
        blank=True,
        help_text='Kanoniczny URL (puste = auto z get_absolute_url).'
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def save(self, *args, **kwargs):
        # Auto-calculate reading time: ~200 words per minute, min 1 minute
        if self.body:
            word_count = len(self.body.split())
            self.reading_time = max(1, word_count // 200)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )

    def get_meta_description(self):
        """Zwraca meta description: custom → excerpt → body[:160]."""
        if self.meta_description:
            return self.meta_description
        if self.excerpt:
            return self.excerpt[:160]
        plain = re.sub(r'[#*`\[\]()>]', '', self.body)
        return plain[:160].strip()

    def get_canonical_url(self, request=None):
        """Zwraca kanoniczny URL (custom lub auto)."""
        if self.canonical_url:
            return self.canonical_url
        url = self.get_absolute_url()
        if request:
            return request.build_absolute_uri(url)
        return url

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_comments',
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
