from django.conf import settings

SITE_NAME = getattr(settings, 'SITE_NAME', 'DevLog')
SITE_URL = getattr(settings, 'SITE_URL', 'https://devlog.example.com')
SITE_DESCRIPTION = getattr(settings, 'SITE_DESCRIPTION', 'Blog o cyklu tworzenia aplikacji webowej')
SITE_IMAGE = getattr(settings, 'SITE_DEFAULT_OG_IMAGE', '')
TWITTER_HANDLE = getattr(settings, 'TWITTER_HANDLE', '')


def seo_defaults(request):
    return {
        'SITE_NAME': SITE_NAME,
        'SITE_URL': SITE_URL,
        'SITE_DESCRIPTION': SITE_DESCRIPTION,
        'SITE_DEFAULT_IMAGE': SITE_IMAGE,
        'TWITTER_HANDLE': TWITTER_HANDLE,
    }
