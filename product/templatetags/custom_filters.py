from django import template

register = template.Library()


@register.filter
def split(value, delimiter=","):
    """Splits the string by the given delimiter."""
    return value.split(delimiter)
