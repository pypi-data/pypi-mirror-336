'''
https://stackoverflow.com/questions/60132733/django-include-templates-in-markdown

https://stackoverflow.com/questions/73807788/python-django-render-to-string-outpu-rendered-as-text-with-html-entities

added this extension in 2025 to get target="_blank" functionality for links
https://github.com/Phuker/markdown_link_attr_modifier
'''
import markdown
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


extensions = [
    'markdown_link_attr_modifier',
]
extension_configs = {
    'markdown_link_attr_modifier': {
        'new_tab': 'on',
        'no_referrer': 'external_only',
        'auto_title': 'on',
    },
}

register = template.Library()

@register.simple_tag(takes_context=True)
def include_md(context, template_name):
    rendered = render_to_string(template_name, context={})
    return mark_safe(markdown.markdown(rendered,
        extensions=extensions,
        extension_configs=extension_configs))


'''
from django.template.defaultfilters import stringfilter
import markdown as md

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])

# https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#code-layout
# https://learndjango.com/tutorials/django-markdown-tutorial
'''