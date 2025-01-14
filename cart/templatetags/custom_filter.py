from django import template

register = template.Library()


@register.filter
def split(value, delimiter=","):
    """Splits the string by the given delimiter."""
    return value.split(delimiter)


@register.filter
def sum(dict):
    total = 0

    for key in dict:
        total += key.selling_price

    return total
