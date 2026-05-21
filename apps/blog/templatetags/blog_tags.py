"""
Custom template tags and filters for the blog app.
"""
import bleach
from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify as _markdownify

register = template.Library()

# Allowed HTML tags after Markdown rendering (bleach sanitize)
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'b', 'i', 'u', 's', 'del',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'dl', 'dt', 'dd',
    'a', 'img',
    'blockquote', 'pre', 'code',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'hr', 'div', 'span',
]

ALLOWED_ATTRIBUTES = {
    'a':   ['href', 'title', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'code': ['class'],
    'pre':  ['class'],
    'span': ['class'],
    'div':  ['class'],
    'th':   ['scope'],
    'td':   ['colspan', 'rowspan'],
}


@register.filter(name='markdownify', is_safe=True)
def markdownify(value):
    """
    Convert Markdown text to sanitized HTML.
    Usage: {{ post.body|markdownify }}
    """
    if not value:
        return ''
    html = _markdownify(value)
    # Sanitize with bleach to prevent XSS
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=False,
    )
    return mark_safe(clean_html)
