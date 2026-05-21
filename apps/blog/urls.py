from django.urls import path

from . import views
from .feeds import CategoryFeed, LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('search/', views.post_search, name='post_search'),
    path('tag/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),
    path('category/<slug:cat_slug>/', views.CategoryPostListView.as_view(), name='post_list_by_category'),
    path('author/<str:username>/', views.AuthorPostListView.as_view(), name='post_list_by_author'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail',
    ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    # RSS Feeds
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('feed/category/<slug:cat_slug>/', CategoryFeed(), name='category_feed'),
]
