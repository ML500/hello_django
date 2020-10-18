import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import View
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.serializers import ArticleSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return JsonResponse(slr.data, safe=False)


class ArticleCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class ArticleUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        object = get_object_or_404(Article, id=kwargs['pk'])
        serializer = ArticleSerializer(data=request.data, instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Article, id=kwargs['pk'])
        slr = ArticleSerializer(object)
        return JsonResponse(slr.data, safe=False)


class ArticleDeleteView(View):
    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(Article, id=kwargs['pk'])
        object.delete()
        return JsonResponse({'pk': kwargs['pk']}, safe=False)

# class ArticleUpdateView(View):
#     def put(self, request, *args, **kwargs):
#         object = get_object_or_404(Article, id=kwargs['pk'])
#         data = json.loads(request.body)
#         serializer = ArticleSerializer(data=data, instance=object)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, safe=False)
#         else:
#             response = JsonResponse(serializer.errors, safe=False)
#             response.status_code = 400
#             return response


# class ArticleCreateView(View):
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         slr = ArticleSerializer(data=data)
#         if slr.is_valid():
#             article = slr.save()
#             return JsonResponse(slr.data, safe=False)
#         else:
#             response = JsonResponse(slr.errors, safe=False)
#             response.status_code = 400
#             return response

# if not request.user.is_authenticated:
#     response = JsonResponse({
#         'error': 'Forbidden'
#     })
#     response.status_code = 403
#     return response
# data = json.loads(request.body)
# print(data)
# article = Article.objects.create(
#     author_id=self.request.user,
#     title=data['title'],
#     text=data['text']
# )
# return JsonResponse({
#     'pk': article.pk,
#     'author_id': article.author.id,
#     'title': article.title,
#     'text:': article.text,
#     'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#     'updated_at': article.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
# })


# class ArticleUpdateView(View):
#     def put(self, request, *args, **kwargs):
#         object = get_object_or_404(Article, id=kwargs['pk'])
#         data = json.loads(request.body)
#         serializer = ArticleSerializer(data=data, instance=object)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, safe=False)
#         else:
#             response = JsonResponse(serializer.errors, safe=False)
#             response.status_code = 400
#             return response
