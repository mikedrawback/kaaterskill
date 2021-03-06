Kaaterskill
============
A minimal, hypermedia blog engine based on the [DocJSON document format](https://github.com/docjson/docjson) for [Django](https://www.djangoproject.com/) built with the [Django REST framework](http://django-rest-framework.org/).


Installation
============
    
Install from github:

``` $pip install git+git://github.com/mikedrawback/kaaterskill ```

Add the apps below to your installed apps in ``` settings.py ```:

    INSTALLED_APPS = (
        '...',
        'rest_framework',
        'kaaterskill',
        'kaaterskill.blog',
        '...'
    )

Add urls to your ``` urls.py ```:

    import kaaterskill.blog.urls

    urlpatterns = patterns('',
        ...
        url(r'^blog/', include(kaaterskill.blog.urls)),
    )

Setup
============

Change the title of your blog in your project's ``` settings.py ```:

    KAATERSKILL_SETTINGS = {'title': 'My Blog'}

Set your Django REST Framework renderers in ``` settings.py ```:

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework_docjson.renderers.DocJSONRenderer',
            'rest_framework.renderers.TemplateHTMLRenderer',
        )
    }
