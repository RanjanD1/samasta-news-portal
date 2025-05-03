from django.urls import path
from .views import (
    CategoryListCreateView,
    NewsListCreateView,
    NewsRetrieveUpdateDestroyView,
    CommentListCreateView,
    ReporterNewsListView    
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('', NewsListCreateView.as_view(), name='news-list'),
    path('<int:pk>/', NewsRetrieveUpdateDestroyView.as_view(), name='news-detail'),
    path('<int:news_id>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('reporter/', ReporterNewsListView.as_view(), name='reporter-news'),
]