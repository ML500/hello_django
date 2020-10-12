from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.timezone import make_naive
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from webapp.models import Article, Tag, ArticleLike
from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT
from .base_views import SearchView


class IndexView(SearchView):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    paginate_by = 2
    paginate_orphans = 0
    model = Article
    ordering = ['-created_at']
    search_fields = ['title__icontains', 'author__i contains']

    def get_queryset(self):
        data = super().get_queryset()
        if not self.request.GET.get('is_admin', None):
            data = data.filter(status='moderated')
        return data


@login_required
def article_mass_action_view(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_articles', [])
        if 'delete' in request.POST:
            Article.objects.filter(id__in=ids).delete()
    return redirect('index')


class ArticleView(DetailView):
    template_name = 'article/article_view.html'
    model = Article
    paginate_comments_by = 2
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments, page, is_paginated = self.paginate_comments(self.object)
        context['comments'] = comments
        context['page_obj'] = page
        context['is_paginated'] = is_paginated  # page.has_other_pages()
        print(self.args)
        print(self.kwargs)
        return context

    def paginate_comments(self, article):
        comments = article.comments.all().order_by('-created_at')
        if comments.count() > 0:
            paginator = Paginator(comments, self.paginate_comments_by, orphans=self.paginate_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1
            return page.object_list, page, is_paginated
        else:
            return comments, None, False


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/article_create.html'
    form_class = ArticleForm
    model = Article

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     response = super().form_valid(form)
    #     tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
    #     form.instance.tags.add(tag)
    #     return response
    #
    # def get_success_url(self):
    #     return reverse('article_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        form.save_m2m()
        tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
        article.tags.add(tag)
        return redirect('article_view', pk=article.pk)


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'article/article_update.html'
    form_class = ArticleForm
    model = Article
    permission_required = 'webapp.change_article'

    def has_permission(self):
        article = self.get_object()
        return super().has_permission() or article.author == self.request.user

    # def dispatch(self, request, *args, **kwargs):
    #     user = request.user
    #     if not user.is_authenticated:
    #         return redirect('accounts:login')
    #     if not user.has_perm('webapp.change_article'):
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'publish_at': make_naive(self.object.publish_at) \
            .strftime(BROWSER_DATETIME_FORMAT)}

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
    #     form.instance.tags.add(tag)
    #     return response

    # def get_success_url(self):
    #     return reverse('article_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        article = form.save()
        tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
        article.tags.add(tag)
        return redirect('article_view', pk=article.pk)


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'article/delete_article.html'
    model = Article
    success_url = reverse_lazy('index')

    # permission_required = 'webapp.delete_article'

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_article') or \
               self.get_object().author == self.request.user


class ArticleLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
        if created:
            article.like_count += 1
            article.save()
            return HttpResponse(article.like_count)
        else:
            return HttpResponseForbidden()


class ArticleUnLikeView(LoginRequiredMixin ,View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        like = get_object_or_404(article.likes, user=request.user)
        like.delete()
        article.like_count -= 1
        article.save()
        return HttpResponse(article.like_count)
