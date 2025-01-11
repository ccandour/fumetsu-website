from django import template
from django.urls import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context, url_name):
    try:
        return 'active' if resolve(context['request'].path_info).url_name == url_name else ''
    except:
        return ''


@register.filter(name='convert_markdown')
def convert_markdown(text):
    from markdown import markdown
    extensions = ['markdown_link_attr_modifier', ]
    extension_configs = {
        'markdown_link_attr_modifier': {
            'new_tab': 'on',
            'no_referrer': 'external_only',
            'auto_title': 'on',
        },
    }
    return markdown(text, extensions=extensions, extension_configs=extension_configs)


@register.filter(name='large_to_medium')
def large_to_medium(value):
    return value.replace('large', 'medium')


@register.filter
def trimwords(value, arg):
    """Truncates a string after a certain number of words."""
    length = int(arg)
    words = value.split()
    if len(words) > length:
        words = words[:length]
        if words[-1].endswith('.') or words[-1].endswith('!') or words[-1].endswith('?') or words[-1].endswith(':') or \
                words[-1].endswith(';') or words[-1].endswith(',') or words[-1].endswith(' '):
            words = words[:-1]

    joined = ' '.join(words)
    if not joined.endswith('...') and len(joined) < len(value):
        return joined + '...'
    return joined


@register.filter
def strip(value):
    return value.strip()


@register.filter
def add_two_sizes(value, arg):
    return len(value) + len(arg)
