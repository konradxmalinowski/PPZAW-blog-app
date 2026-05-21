from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),
    path('category/<slug:cat_slug>/', views.CategoryPostListView.as_view(), name='post_list_by_category'),
    path('author/<str:username>/', views.AuthorPostListView.as_view(), name='post_list_by_author'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail',
    ),
]
