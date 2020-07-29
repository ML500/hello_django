from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from webapp.models import Article, STATUS_CHOICES
from webapp.forms import ArticleForm


def index_view(request):
    data = Article.objects.all()
    return render(request, 'index.html', context={
        'articles': data
    })


def article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, 'article_view.html', context)


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html', context={
            'form': ArticleForm()
        })
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            # article = Article.objects.create(**form.cleaned_data)
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                author=form.cleaned_data['author'],
                status=form.cleaned_data['status'],
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
            'status': article.status
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
