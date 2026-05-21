from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.blog.models import Post, Category
from apps.api.serializers import (
    PostListSerializer, PostDetailSerializer, PostWriteSerializer,
    CategorySerializer, CommentSerializer,
)
from apps.api.permissions import IsAuthorOrReadOnly


class PostListCreateAPIView(generics.ListCreateAPIView):
    """GET: lista postów; POST: utwórz post (auth)."""

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body', 'excerpt']
    ordering_fields = ['publish', 'reading_time']
    ordering = ['-publish']

    def get_queryset(self):
        qs = Post.published.all()
        tag = self.request.query_params.get('tag')
        cat = self.request.query_params.get('category')
        if tag:
            qs = qs.filter(tags__slug=tag)
        if cat:
            qs = qs.filter(category__slug=cat)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostWriteSerializer
        return PostListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET: szczegóły; PUT/PATCH: edycja (author/admin); DELETE: usuń (author/admin)."""

    queryset = Post.published.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostWriteSerializer
        return PostDetailSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, slug=self.kwargs['slug'], status='published')
        return post.comments.filter(active=True)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, slug=self.kwargs['slug'], status='published')
        user = self.request.user
        serializer.save(
            post=post,
            user=user,
            name=user.get_full_name() or user.username,
            email=user.email,
        )


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TagListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from taggit.models import Tag
        from django.db.models import Count
        tags = (
            Tag.objects
            .annotate(count=Count('taggit_taggeditem_items'))
            .order_by('-count')
        )
        data = [
            {'name': t.name, 'slug': t.slug, 'count': t.count}
            for t in tags
        ]
        return Response(data)
