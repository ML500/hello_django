from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.utils.timezone import make_naive
from django.views.generic import View, TemplateView, FormView

from webapp.models import Article
from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT
from .base_views import FormView as CustomFormView, ListView as CustomListVIew


class IndexView(CustomListVIew):
    template_name = 'index.html'
    context_key = 'articles'

    def get_queryset(self):
        data = Article.objects.all()

        if not self.request.GET.get('is_admin', None):
            data = Article.objects.filter(status='moderated')

        search = self.request.GET.get('search')
        if search:
            data = data.filter(title__icontains=search)

        return data
        # return render(self.request, 'index.html', context={
        #     'articles': data
        # })


class ArticleView(TemplateView):
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)

        context['article'] = article
        return context


class ArticleCreateView(CustomFormView):
    template_name = 'article_create.html'
    form_class = ArticleForm

    def form_valid(self, form):
        self.article = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('article_view', kwargs={'pk': self.article.pk})


class ArticleUpdateView(FormView):
    template_name = 'article_update.html'
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.get_object()
        return context

    def get_initial(self):
        return {'publish_at': datetime.now().strftime(BROWSER_DATETIME_FORMAT)}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def form_valid(self, form):
        self.article = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.article})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete_article.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
