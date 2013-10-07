from django.conf import settings


KAATERSKILL_SETTINGS = getattr(settings, 'KAATERSKILL_SETTINGS',
                               {'title': 'Kaaterskill'})
