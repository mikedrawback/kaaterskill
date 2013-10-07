from django.contrib import admin
from django.db import models
from django.utils import importlib

blog_app = models.get_app("blog")
blog_models = importlib.import_module(blog_app.__name__[:-6] + "models")

Category = blog_models.Category
Tag = blog_models.Tag
Article = blog_models.Article


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)
