import os

from django import template
from django.contrib.auth.models import Group
from django.urls import resolve

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except:
        return False  # group doesn't exist, so for sure the user isn't part of the group

    # for superuser or staff, always return True
    if user.is_superuser or user.is_staff:
        return True

    return user.groups.filter(name=group_name).exists()


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