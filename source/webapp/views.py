from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_naive
from django.http import HttpResponseNotAllowed
from django.views.generic import View, TemplateView

from webapp.models import Article
from webapp.forms import ArticleForm


class IndexView(View):
    def get(self, request):
        is_admin = request.GET.get('is_admin', None)
        if is_admin:
            data = Article.objects.all()
        else:
            data = Article.objects.filter(status='moderated')
        return render(request, 'index.html', context={
            'articles': data
        })


class ArticleView(TemplateView):
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)

        context['article'] = article
        return context


class ArticleCreateView(View):
    def get(self, request):
        return render(request, 'article_create.html', context={
            'form': ArticleForm()
        })

    def post(self, request):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            # article = Article.objects.create(**form.cleaned_data)
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                author=form.cleaned_data['author'],
                status=form.cleaned_data['status'],
                publish_at=form.cleaned_data['publish_at']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article_create.html', context={
                'form': form
            })


# def delete_article(request):
#     if request.method == 'GET':
#         return render(request, 'delete_form.html')
#     elif request.method == 'POST':
#         id_article = request.POST.get('id')
#         article = Article.objects.get(pk=id_article)
#         article.delete()
#         data = Article.objects.all()
#         return render(request, 'index.html', context={
#             'articles': data
#         })
def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        form = ArticleForm(initial={
            'title': article.title,
            'text': article.text,
            'author': article.author,
            'status': article.status,
            'publish_at': make_naive(article.publish_at).strftime('%Y-%m-%dT%H:%M')
            # 'publish_at': article.publish_at
        })
        return render(request, 'article_update.html', context={
            'form': form,
            'article': article
        })
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            # article = Article.objects.create(**form.cleaned_data)
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            article.status = form.cleaned_data['status']
            article.publish_at = form.cleaned_data['publish_at']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article_update.html', context={
                'article': article,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete_article.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
