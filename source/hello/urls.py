"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from webapp.views import IndexView, ArticleCreateView, ArticleView, \
    ArticleUpdateView, ArticleCommentCreateView, article_mass_action_view, CommentUpdateView, \
    ArticleDeleteView, CommentDeleteViews, ArticleLike, ArticleLikeView, ArticleUnLikeView, CommentLikeView, \
    CommentUnLikeView
from django.conf.urls.static import static
from django.conf import settings
# from accounts.views import login_view, logout_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', IndexView.as_view(), name='index'),
                  path('article/', include([
                      path('add/', ArticleCreateView.as_view(), name='article_create'),
                      path('<int:pk>/', ArticleView.as_view(), name='article_view'),
                      path('<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
                      path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
                      path('mass-action/', article_mass_action_view, name='article_mass_action'),
                      path('<int:pk>/comments/add/', ArticleCommentCreateView.as_view(),
                           name='article_comment_add'),
                      path('<int:pk>/like/', ArticleLikeView.as_view(), name='article_like'),
                      path('<int:pk>/unlike/', ArticleUnLikeView.as_view(), name='article_unlike')
                  ])),

                  path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
                  path('comment/<int:pk>/delete/', CommentDeleteViews.as_view(), name='comment_delete'),
                  path('<int:pk>/like/', CommentLikeView.as_view(), name='comment_like'),
                  path('<int:pk>/unlike/', CommentUnLikeView.as_view(), name='comment_unlike'),

                  path('accounts/', include('accounts.urls')),
                  path('api/v1/',include('api_v1.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
