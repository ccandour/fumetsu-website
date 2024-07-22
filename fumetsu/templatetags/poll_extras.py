from django import template

register = template.Library()


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
