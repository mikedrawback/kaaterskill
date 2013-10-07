from django.utils import importlib
from django.db import models
from kaaterskill_settings import KAATERSKILL_SETTINGS

from rest_framework.response import Response
from rest_framework.views import APIView

blog_app = models.get_app("blog")
blog_serializers = importlib.import_module(blog_app.__name__[:-6] + "serializers")
blog_models = importlib.import_module(blog_app.__name__[:-6] + "models")

ArticleListDocumentSerializer = blog_serializers.ArticleListDocumentSerializer
ArticleDetailDocumentSerializer = blog_serializers.ArticleDetailDocumentSerializer

Category = blog_models.Category
Tag = blog_models.Tag
Article = blog_models.Article


# Document objects to be serialized

class NavigationDocument(object):
    title = KAATERSKILL_SETTINGS['title']
    categories = Category.objects.published()
    archive = Article.objects.published().dates('date_published', 'month', order='DESC')
    tags = Tag.objects.published()


class ArticleListDocument(NavigationDocument):
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def articles(self):
        return Article.objects.published().filter(**self.kwargs)


class ArticleDetailDocument(NavigationDocument):
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def article(self):
       return Article.objects.published().get(**self.kwargs)


# API View classes

class ArticleDetail(APIView):
    article_document_class = ArticleDetailDocument

    def get(self, request, *args, **kwargs):
        document = self.article_document_class(**kwargs)
        serializer = ArticleDetailDocumentSerializer(document, context={'request': request})

        return Response(serializer.data, template_name='blog.html')


class ArticleList(APIView):
    article_document_class = ArticleListDocument

    def get(self, request, *args, **kwargs):
        document = self.article_document_class(**kwargs)
        serializer = ArticleListDocumentSerializer(document, context={'request': request})
        
        return Response(serializer.data, template_name='blog.html')


class BlogRoot(ArticleList):
    pass
