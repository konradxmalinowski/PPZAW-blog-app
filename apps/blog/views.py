from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from taggit.models import Tag

from apps.blog.forms import CommentForm, EmailPostForm, SearchForm
from apps.blog.models import Comment, Category, Post


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
    """FBV — post detail with comments and similar posts by shared tags."""
    post_obj = get_object_or_404(
        Post,
        status='published',
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # Active comments for this post, oldest first
    comments = post_obj.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post_obj
            # Auto-associate authenticated user; override name/email to match account
            if request.user.is_authenticated:
                new_comment.user = request.user
                new_comment.name = request.user.get_full_name() or request.user.username
                new_comment.email = request.user.email
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Similar posts: posts sharing the most tags, excluding current post
    post_tags_ids = post_obj.tags.values_list('id', flat=True)
    similar_posts = (
        Post.published
        .filter(tags__in=post_tags_ids)
        .exclude(id=post_obj.id)
        .annotate(same_tags=Count('tags'))
        .order_by('-same_tags', '-publish')[:4]
    )

    return render(request, 'blog/post_detail.html', {
        'post': post_obj,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'section': 'blog',
    })


def post_share(request, post_id):
    """FBV — email-share a published post. Sends via EMAIL_BACKEND (console in dev)."""
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} ({cd["email"]}) poleca: "{post.title}"'
            message = (
                f'Przeczytaj post "{post.title}" na:\n{post_url}\n\n'
                f'Komentarz od {cd["name"]}:\n{cd["comments"]}'
            )
            send_mail(subject, message, 'devlog@example.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post_share.html', {
        'post': post,
        'form': form,
        'sent': sent,
        'section': 'blog',
    })


def post_search(request):
    """FBV — basic full-text search using Q-objects (icontains on title/body/excerpt)."""
    form = SearchForm()
    results = []
    query = None

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.filter(
                Q(title__icontains=query)
                | Q(body__icontains=query)
                | Q(excerpt__icontains=query)
            ).distinct()

    return render(request, 'blog/post_search.html', {
        'form': form,
        'query': query,
        'results': results,
        'section': 'search',
    })
