from django.conf.urls import patterns, include, url, RegexURLResolver
from django.db import models
from django.utils import importlib

blog_app = models.get_app("blog")
blog_views = importlib.import_module(blog_app.__name__[:-6] + "views")

BlogRoot = blog_views.BlogRoot
ArticleDetail = blog_views.ArticleDetail
ArticleList = blog_views.ArticleList

urlpatterns = patterns('',

    url(r'^$', BlogRoot.as_view(), name='blog-root'),

    url(r'^articles', include(patterns('',
        url(r'^/(?P<slug>.+)/$', ArticleDetail.as_view(), name='article-detail'),
    ))),

    url(r'^category', include(patterns('',
        url(r'^/(?P<category__slug>.+)$', ArticleList.as_view(), name='articlesbycategory-list'),
    ))),

    url(r'^tag', include(patterns('',
        url(r'^/(?P<tags__slug>.+)$', ArticleList.as_view(), name='articlesbytag-list'),
    ))),

    url(r'^archive', include(patterns('',
        url(r'^/(?P<date_published__year>.+)/(?P<date_published__month>.+)$', ArticleList.as_view(), name='articlesbyarchive-list'),
    ))),
)
