from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from taggit.models import Tag

from .models import Post, Category


class PostListView(ListView):
    queryset = Post.published.all()
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        return context


def post_list_by_tag(request, tag_slug):
    """FBV — lists published posts filtered by a taggit tag slug."""
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.published.filter(tags__in=[tag])

    # Manual pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return _render_post_list(
        request,
        page_obj,
        tag=tag,
        section='blog',
    )


def _render_post_list(request, page_obj, tag=None, category=None, author=None, section='blog'):
    """Shared render helper for tag/category/author filtered list views."""
    from django.shortcuts import render
    return render(request, 'blog/post_list.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'tag': tag,
        'category': category,
        'author': author,
        'section': section,
    })


class CategoryPostListView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Post.published.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['section'] = 'blog'
        return context


class AuthorPostListView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.published.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        context['section'] = 'blog'
        return context


def post_detail(request, year, month, day, post):
    """FBV — post detail with similar posts by shared tags."""
    from django.db.models import Count

    post_obj = get_object_or_404(
        Post,
        status='published',
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # Similar posts: posts sharing the most tags, excluding current post
    post_tags_ids = post_obj.tags.values_list('id', flat=True)
    similar_posts = (
        Post.published
        .filter(tags__in=post_tags_ids)
        .exclude(id=post_obj.id)
        .annotate(same_tags=Count('tags'))
        .order_by('-same_tags', '-publish')[:4]
    )

    from django.shortcuts import render
    return render(request, 'blog/post_detail.html', {
        'post': post_obj,
        'similar_posts': similar_posts,
        'section': 'blog',
    })
