from django.shortcuts import render, redirect
from webapp.models import Article, STATUS_CHOICES
from django.http import HttpResponseNotAllowed


def index_view(request):
    data = Article.objects.all()
    return render(request, 'index.html', context={
        'articles': data
    })


def article_view(request):
    article_id = request.GET.get('pk')
    article = Article.objects.get(pk=article_id)
    context = {'article': article}
    return render(request, 'article_view.html', context)


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html', context={'status_choices': STATUS_CHOICES
                                                               })
    elif request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        author = request.POST.get('author')
        status = request.POST.get('status')
        article = Article.objects.create(title=title, text=text, author=author, status=status)

        return redirect(f'/article/?pk={article.pk}')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def delete_article(request):
    if request.method == 'GET':
        return render(request, 'delete_form.html')
    elif request.method == 'POST':
        id_article = request.POST.get('id')
        article = Article.objects.get(pk=id_article)
        article.delete()
        data = Article.objects.all()
        return render(request, 'index.html', context={
            'articles': data
        })
