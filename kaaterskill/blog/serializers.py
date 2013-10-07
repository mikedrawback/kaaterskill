from django.utils import importlib
from django.db import models

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from rest_framework_docjson.fields import DocJSONIdentityField
from rest_framework_docjson.serializers import DocJSONModelSerializer, DocJSONSerializer
from rest_framework_docjson.reverse import reverse

blog_app = models.get_app("blog")
blog_models = importlib.import_module(blog_app.__name__[:-6] + "models")

Category = blog_models.Category
Tag = blog_models.Tag
Article = blog_models.Article


class CategorySerializer(DocJSONModelSerializer):
    permalink = serializers.SerializerMethodField('posts_by_category')

    def posts_by_category(self, obj):
        return reverse('articlesbycategory-list',
                       args=[obj.slug],
                       request=self.context['request'])

    class Meta:
        model = Category
        fields = ('name', 'permalink')


class TagSerializer(DocJSONModelSerializer):
    permalink = serializers.SerializerMethodField('posts_by_tag')

    def posts_by_tag(self, obj):
        return reverse('articlesbytag-list',
                       args=[obj.slug],
                       request=self.context['request'])

    class Meta:
        model = Tag
        fields = ('name', 'permalink')


class ArticleListSerializer(DocJSONModelSerializer):
    permalink = DocJSONIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        lookup_field = 'slug'
        fields = ('title', 'body', 'permalink', 'date_published')


class ArticleDetailSerializer(DocJSONModelSerializer):
    permalink = DocJSONIdentityField(view_name='article-detail')
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        lookup_field = 'slug'
        fields = ('title',
                  'body',
                  'published',
                  'permalink',
                  'date_published',
                  'tags')


class ArticleMonthSerializer(DocJSONSerializer):
    permalink = serializers.SerializerMethodField('get_permalink')
    name = serializers.SerializerMethodField('get_name')

    def get_permalink(self, obj):
        return reverse('articlesbyarchive-list',
                       request=self.context['request'],
                       args=[obj.year, obj.month])

    def get_name(self, obj):
        date_format = self.context.get('archive_date_format', '%B, %Y')
        return obj.strftime(date_format)


class NavigationDocumentSerializer(DocJSONSerializer):
    title = serializers.CharField()
    categories = CategorySerializer(many=True)
    archive = ArticleMonthSerializer(many=True)
    tags = TagSerializer(many=True)
    navigation = serializers.SerializerMethodField('get_navbar')

    def get_navbar(self, obj):
        return {'blog': reverse('blog-root', request=self.context['request'])}


class ArticleListDocumentSerializer(NavigationDocumentSerializer):
    articles = ArticleListSerializer(many=True)


class ArticleDetailDocumentSerializer(NavigationDocumentSerializer):
    article = ArticleDetailSerializer(many=False)
