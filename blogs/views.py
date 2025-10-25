# blogs/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from .models import Post, Category
from .serializers import PostListSerializer, PostDetailSerializer

class BlogPagination(PageNumberPagination):
    page_size = 6  # Match your frontend pagination
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'content']
    filterset_fields = ['categories__slug']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        queryset = Post.objects.filter(draft=False).select_related('author').prefetch_related('categories')
        
        # Filter by category if provided
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
            
        return queryset

class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(draft=False).select_related('author').prefetch_related('categories', 'tags')

class RecentPostsView(generics.ListAPIView):
    serializer_class = PostListSerializer
    
    def get_queryset(self):
        return Post.objects.filter(draft=False).order_by('-date')[:5]

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    data = [{'name': cat.name, 'slug': cat.slug} for cat in categories]
    return Response(data)