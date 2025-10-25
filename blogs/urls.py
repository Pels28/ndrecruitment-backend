# blogs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('recent-posts/', views.RecentPostsView.as_view(), name='recent-posts'),
    path('categories/', views.category_list, name='category-list'),
]