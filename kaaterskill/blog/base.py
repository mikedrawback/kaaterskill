from django.db import models
from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from model_utils.managers import PassThroughManager


class CategoryQuerySet(QuerySet):
    def published(self):
        return self.filter(article__published=True).distinct()


class CategoryBase(models.Model):
    objects = PassThroughManager.for_queryset_class(CategoryQuerySet)()

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=80, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(CategoryBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'blog'
        verbose_name_plural = 'Categories'


class TagQuerySet(QuerySet):
    def published(self):
        return self.filter(article__published=True).distinct()


class TagBase(models.Model):
    objects = PassThroughManager.for_queryset_class(TagQuerySet)()

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=80, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(TagBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'blog'


class ArticleQuerySet(QuerySet):
    def published(self):
        return self.filter(published=True)


class ArticleBase(models.Model):
    objects = PassThroughManager.for_queryset_class(ArticleQuerySet)()

    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User)
    category = models.ForeignKey('blog.Category', null=True, blank=True)
    tags = models.ManyToManyField('blog.Tag', null=True, blank=True)
    date_published = models.DateTimeField()
    published = models.BooleanField()
    slug = models.SlugField(max_length=300, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(ArticleBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'blog'
        ordering = ['-date_published']
