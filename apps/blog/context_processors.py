from .models import Category, Post
from taggit.models import Tag


def sidebar_context(request):
    """
    Global sidebar context: recent posts, categories, popular tags.
    Added to TEMPLATES context_processors in settings.
    """
    categories = Category.objects.all()
    popular_tags = Tag.objects.all()[:20]
    return {
        'categories': categories,
        'popular_tags': popular_tags,
    }
