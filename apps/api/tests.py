from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.blog.models import Post, Category, Comment


class APITestBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user('author', 'author@example.com', 'pass12345')
        cls.other = User.objects.create_user('other', 'other@example.com', 'pass12345')
        cls.admin = User.objects.create_user('admin', 'admin@example.com', 'pass12345', is_staff=True)

        cls.category = Category.objects.create(name='Backend', slug='backend', color='#79c0ff')

        cls.published = Post.objects.create(
            title='Published Post',
            slug='published-post',
            author=cls.author,
            category=cls.category,
            body='word ' * 100,
            excerpt='An excerpt',
            status='published',
            publish=timezone.now(),
        )
        cls.published.tags.add('django', 'rest')

        cls.related = Post.objects.create(
            title='Related Post',
            slug='related-post',
            author=cls.author,
            body='word ' * 50,
            status='published',
            publish=timezone.now(),
        )
        cls.related.tags.add('django')

        cls.draft = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            author=cls.author,
            body='word ' * 30,
            status='draft',
            publish=timezone.now(),
        )

        Comment.objects.create(
            post=cls.published, user=cls.author, name='author',
            email='author@example.com', body='Active comment', active=True,
        )
        Comment.objects.create(
            post=cls.published, name='spam',
            email='spam@example.com', body='Hidden comment', active=False,
        )

    def auth(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def logout(self):
        self.client.credentials()


class PostListTests(APITestBase):
    def test_list_returns_paginated_published_only(self):
        resp = self.client.get('/api/posts/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('results', resp.data)
        self.assertIn('count', resp.data)
        slugs = [p['slug'] for p in resp.data['results']]
        self.assertIn('published-post', slugs)
        self.assertNotIn('draft-post', slugs)

    def test_list_has_reading_bar(self):
        resp = self.client.get('/api/posts/')
        first = resp.data['results'][0]
        self.assertIn('reading_bar', first)
        self.assertEqual(len(first['reading_bar']), 10)

    def test_filter_by_tag(self):
        resp = self.client.get('/api/posts/?tag=rest')
        slugs = [p['slug'] for p in resp.data['results']]
        self.assertEqual(slugs, ['published-post'])

    def test_filter_by_category(self):
        resp = self.client.get('/api/posts/?category=backend')
        slugs = [p['slug'] for p in resp.data['results']]
        self.assertEqual(slugs, ['published-post'])

    def test_search(self):
        resp = self.client.get('/api/posts/?search=Published')
        slugs = [p['slug'] for p in resp.data['results']]
        self.assertIn('published-post', slugs)


class PostDetailTests(APITestBase):
    def test_detail_includes_active_comments_and_count(self):
        resp = self.client.get('/api/posts/published-post/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['comments_count'], 1)
        self.assertEqual(len(resp.data['comments']), 1)
        self.assertEqual(resp.data['comments'][0]['body'], 'Active comment')

    def test_detail_includes_similar_posts(self):
        resp = self.client.get('/api/posts/published-post/')
        similar_slugs = [p['slug'] for p in resp.data['similar_posts']]
        self.assertIn('related-post', similar_slugs)
        self.assertNotIn('published-post', similar_slugs)

    def test_draft_not_accessible(self):
        resp = self.client.get('/api/posts/draft-post/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class PostCreateTests(APITestBase):
    payload = {
        'title': 'New API Post',
        'body': 'word ' * 60,
        'excerpt': 'made via API',
        'tags': ['api', 'new'],
        'status': 'published',
    }

    def test_create_requires_auth(self):
        resp = self.client.post('/api/posts/', self.payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_token(self):
        self.auth(self.author)
        resp = self.client.post('/api/posts/', self.payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        created = Post.objects.get(title='New API Post')
        self.assertEqual(created.author, self.author)
        self.assertEqual(set(created.tags.names()), {'api', 'new'})

    def test_create_without_tags(self):
        self.auth(self.author)
        payload = {k: v for k, v in self.payload.items() if k != 'tags'}
        payload['title'] = 'No Tags Post'
        resp = self.client.post('/api/posts/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class PostMutationPermissionTests(APITestBase):
    def test_non_author_cannot_delete(self):
        self.auth(self.other)
        resp = self.client.delete('/api/posts/published-post/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_delete(self):
        self.auth(self.author)
        resp = self.client.delete('/api/posts/published-post/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_delete_others_post(self):
        self.auth(self.admin)
        resp = self.client.delete('/api/posts/published-post/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_author_cannot_patch(self):
        self.auth(self.other)
        resp = self.client.patch('/api/posts/published-post/', {'title': 'Hacked'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_patch(self):
        self.auth(self.author)
        resp = self.client.patch('/api/posts/published-post/', {'title': 'Edited'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.published.refresh_from_db()
        self.assertEqual(self.published.title, 'Edited')


class CommentTests(APITestBase):
    def test_list_only_active(self):
        resp = self.client.get('/api/posts/published-post/comments/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        bodies = [c['body'] for c in resp.data['results']]
        self.assertIn('Active comment', bodies)
        self.assertNotIn('Hidden comment', bodies)

    def test_create_requires_auth(self):
        resp = self.client.post('/api/posts/published-post/comments/',
                                {'body': 'hi'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sets_user_name_email(self):
        self.auth(self.author)
        resp = self.client.post('/api/posts/published-post/comments/',
                                {'body': 'A new comment'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(body='A new comment')
        self.assertEqual(comment.user, self.author)
        self.assertEqual(comment.email, 'author@example.com')

    def test_comments_on_draft_404(self):
        self.auth(self.author)
        resp = self.client.get('/api/posts/draft-post/comments/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class CategoryTagTests(APITestBase):
    def test_categories(self):
        resp = self.client.get('/api/categories/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        names = [c['name'] for c in resp.data['results']]
        self.assertIn('Backend', names)

    def test_tags_with_counts(self):
        resp = self.client.get('/api/tags/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        by_slug = {t['slug']: t for t in resp.data}
        self.assertIn('django', by_slug)
        self.assertEqual(by_slug['django']['count'], 2)


class AuthTokenTests(APITestBase):
    def test_obtain_token(self):
        resp = self.client.post('/api/auth/token/',
                                {'username': 'author', 'password': 'pass12345'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)

    def test_obtain_token_bad_credentials(self):
        resp = self.client.post('/api/auth/token/',
                                {'username': 'author', 'password': 'wrong'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
