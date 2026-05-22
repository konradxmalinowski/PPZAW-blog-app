import pytest
from django.contrib.auth.models import User

from apps.blog.models import Bookmark, Category, Post, PostReaction


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='pass123', email='test@test.com')


@pytest.fixture
def category(db):
    return Category.objects.create(name='Backend', slug='backend')


@pytest.fixture
def post(db, user, category):
    return Post.objects.create(
        title='Test Post',
        slug='test-post',
        author=user,
        category=category,
        body='## Heading One\n\nSome content here.\n\n### Sub heading\n\nMore content.',
        status='published',
    )


class TestPostModel:
    def test_reading_time_calculated(self, post):
        assert post.reading_time >= 1

    def test_get_absolute_url(self, post):
        url = post.get_absolute_url()
        assert 'test-post' in url

    def test_get_meta_description_from_body(self, post):
        desc = post.get_meta_description()
        assert len(desc) <= 160

    def test_published_manager_excludes_draft(self, db, user, category):
        Post.objects.create(
            title='Draft', slug='draft', author=user, category=category,
            body='content', status='draft',
        )
        published = list(Post.published.values_list('slug', flat=True))
        assert 'draft' not in published

    def test_views_count_defaults_to_zero(self, post):
        assert post.views_count == 0


class TestCommentSanitization:
    def test_xss_script_stripped(self, db, post):
        from apps.blog.forms import CommentForm
        form = CommentForm(data={
            'name': 'Attacker',
            'email': 'bad@test.com',
            'body': '<script>alert("xss")</script>Hello',
        })
        assert form.is_valid()
        assert '<script>' not in form.cleaned_data['body']
        assert 'Hello' in form.cleaned_data['body']

    def test_allowed_tags_kept(self, db, post):
        from apps.blog.forms import CommentForm
        form = CommentForm(data={
            'name': 'User',
            'email': 'user@test.com',
            'body': 'Hello <strong>world</strong> and <em>italic</em>',
        })
        assert form.is_valid()
        assert '<strong>' in form.cleaned_data['body']
        assert '<em>' in form.cleaned_data['body']


class TestPostReaction:
    def test_reaction_created(self, db, user, post):
        reaction, created = PostReaction.objects.get_or_create(post=post, user=user)
        assert created
        assert post.reactions.count() == 1

    def test_reaction_unique_per_user(self, db, user, post):
        PostReaction.objects.create(post=post, user=user)
        with pytest.raises(Exception):
            PostReaction.objects.create(post=post, user=user)


class TestBookmark:
    def test_bookmark_created(self, db, user, post):
        bookmark, created = Bookmark.objects.get_or_create(user=user, post=post)
        assert created

    def test_bookmark_unique_per_user_post(self, db, user, post):
        Bookmark.objects.create(user=user, post=post)
        with pytest.raises(Exception):
            Bookmark.objects.create(user=user, post=post)
