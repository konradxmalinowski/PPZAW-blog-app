from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from apps.api import views

app_name = 'api'

urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/comments/', views.CommentListCreateAPIView.as_view(), name='post_comments'),
    path('categories/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('tags/', views.TagListAPIView.as_view(), name='tag_list'),
    path('auth/token/', obtain_auth_token, name='auth_token'),
]
