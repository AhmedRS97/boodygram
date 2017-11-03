from django import template
register = template.Library()

@register.filter
def splitby(iterable, n=1):
    return [iterable[i:i+n] for i in range(0,len(iterable),n)]
    # l = len(iterable)
    # for ndx in range(0, l, n):
    #     return iterable[ndx:min(ndx + n, l)]
