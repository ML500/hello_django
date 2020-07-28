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

        article.title = request.POST.get('title')
        article.text = request.POST.get('text')
        article.author = request.POST.get('author')
        article.status = request.POST.get('status')
        article.save()
        # url = reverse('article_view', kwargs={'pk': article.pk})
        # return redirect(url)
        return redirect('article_view', pk=article.pk)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


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
        return render(request, 'article_update.html', context={'status_choices': STATUS_CHOICES,
                                                               'article': article})
    elif request.method == 'POST':
        errors = {}
        article.title = request.POST.get('title')
        if not article.title:
            errors['title'] = 'This field is required'
        article.text = request.POST.get('text')
        if not article.text:
            errors['text'] = 'This field is required'
        article.author = request.POST.get('author')
        if not article.author:
            errors['author'] = 'This field is required'
        article.status = request.POST.get('status')
        if errors:
            return render(request, 'article_update.html', context={'status_choices': STATUS_CHOICES,
                                                                   'article': article,
                                                                   'errors': errors})
        article.save()
        return redirect('article_view', pk=article.pk)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
