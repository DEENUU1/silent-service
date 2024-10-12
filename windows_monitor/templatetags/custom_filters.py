from django import template

register = template.Library()


@register.filter
def filter_by_disk(queryset, disk):
    return queryset.filter(disk=disk)
