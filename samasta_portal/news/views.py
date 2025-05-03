from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import News, Category, Comment
from .serializers import NewsSerializer, CategorySerializer, CommentSerializer
from accounts.models import CustomUser
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.user_type == 1

class IsReporterOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.user_type in [1, 2])

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_class = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']

class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date', 'views']

    def perform_create(self, serializer):
        if self.request.user.user_type in [1, 2]: #Admin or reporter
            serializer.save(author=self.request.user)

class NewsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsReporterOrAdmin()]
        return [permissions.AllowAny()]

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer

    def get_queryset(self):
        news_id = self.kwargs.get('news_id')
        return self.queryset.filter(news_id=news_id)

    def perform_create(self, serializer):
        news_id = self.kwargs.get('news_id')
        serializer.save(user=self.request.user, news_id=news_id)

class ReporterNewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsReporterOrAdmin]

    def get_queryset(self):
        return News.objects.filter(author=self.request.user)