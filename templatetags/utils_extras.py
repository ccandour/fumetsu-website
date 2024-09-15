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
