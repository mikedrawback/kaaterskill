from django.utils import importlib
from django.db import models
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from rest_framework_docjson.fields import DocJSONIdentityField
from rest_framework_docjson.serializers import DocJSONModelSerializer, DocJSONSerializer
from rest_framework_docjson.pagination import DocJSONPaginationSerializerWithPrevious
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


class AuthorSerializer(DocJSONModelSerializer):
    name = serializers.Field(source='username')
    permalink = serializers.SerializerMethodField('posts_by_author')

    def posts_by_author(self, obj):
        return reverse('articlesbyauthor-list',
                        args=[obj.username],
                        request=self.context['request'])

    class Meta:
        model = User
        fields = ('name', 'permalink')


class ArticleListSerializer(DocJSONModelSerializer):
    permalink = DocJSONIdentityField(view_name='article-detail')
    author = AuthorSerializer()


    class Meta:
        model = Article
        lookup_field = 'slug'
        fields = ('title', 'body', 'permalink', 'date_published', 'author')


class PaginatedArticleSerializer(DocJSONPaginationSerializerWithPrevious):
    class Meta:
        object_serializer_class = ArticleListSerializer


class ArticleDetailSerializer(DocJSONModelSerializer):
    permalink = DocJSONIdentityField(view_name='article-detail')
    author = AuthorSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        lookup_field = 'slug'
        fields = ('title',
                  'body',
                  'published',
                  'permalink',
                  'date_published',
                  'author',
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
        navbar = {'blog': reverse('blog-root', request=self.context['request'])}
        request = self.context['request']
        if request.user.is_authenticated() and request.accepted_renderer.format == 'html':
            try:
                navbar['admin'] = reverse('admin:index', request=request)
            except:
                pass
        return navbar

class ArticleListDocumentSerializer(NavigationDocumentSerializer):
    articles = PaginatedArticleSerializer()


class ArticleDetailDocumentSerializer(NavigationDocumentSerializer):
    article = ArticleDetailSerializer(many=False)
