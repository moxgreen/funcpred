from django import template
from django.template.defaultfilters import stringfilter
import re 

register = template.Library()

@register.filter
@stringfilter
def replace(string,args):
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]
    return re.sub( search, replace, string )

@register.filter
@stringfilter
def keyfy(string):
    string =  re.sub( "_", " ", string )
    tokens = string.split()
    n=256
    if len(tokens)>2:
        n=3
    if len(tokens)>3:
        n=2
    if len(tokens)>4:
        n=1
    return "".join([t[0:n] for t in string.split()])
