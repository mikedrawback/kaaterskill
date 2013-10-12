from django.contrib import admin
from django.db import models
from django.utils import importlib

blog_app = models.get_app("blog")
blog_models = importlib.import_module(blog_app.__name__[:-6] + "models")

Category = blog_models.Category
Tag = blog_models.Tag
Article = blog_models.Article


class ArticleAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('title', 'date_published', 'author')
    list_filter = ('published',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def queryset(self, request):
        if request.user.is_superuser:
            return Article.objects.all()
        return Article.objects.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        has_permission = super(ArticleAdmin, self)\
            .has_change_permission(request, obj)

        if not has_permission:
            return False
        if obj is not None and \
                not request.user.is_superuser and \
                request.user.id != obj.author.id:
            return False
        return True


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)
