"""
Django template tags/filters for correctly linking to Data Central static
resources.
"""

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def dc_static(path):
    """
    Django template tag for static data that isn't JS, CSS or an image, such as
    SEO metadata.
    """
    return settings.DC_STATIC_URL + "/" + path


@register.simple_tag
def dc_static_js(path):
    """
    Django template tag for static JS provided centrally for Data Central.
    """
    return settings.DC_STATIC_URL + "/js/" + path


@register.simple_tag
def dc_static_css(path):
    """
    Django template tag for CSS provided centrally for Data Central.
    """
    return settings.DC_STATIC_URL + "/css/" + path


@register.simple_tag
def dc_static_img(path):
    """
    Django template tag for images provided centrally for Data Central.
    """
    return settings.DC_STATIC_URL + "/img/" + path
