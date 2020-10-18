from django.urls import path

from api_v1.views import get_token_view, ArticleCreateView, ArticleListView, ArticleDetailView, ArticleDeleteView, \
    ArticleUpdateView

app_name = 'api_v1'

urlpatterns = [
    path('get_token/', get_token_view, name='get_token'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(), name='article_detail'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
]
