from django.contrib.syndication.views import Feed
from django.db import models
from django.utils import importlib
from django.core.urlresolvers import reverse

from kaaterskill_settings import KAATERSKILL_SETTINGS

blog_app = models.get_app("blog")
blog_models = importlib.import_module(blog_app.__name__[:-6] + "models")

Article = blog_models.Article


class ArticleFeed(Feed):
    title = KAATERSKILL_SETTINGS['title']
    link = "/feed/"
    description = "Main articles feed"

    def items(self):
        return Article.objects.published()[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('article-detail', args=[item.slug])
