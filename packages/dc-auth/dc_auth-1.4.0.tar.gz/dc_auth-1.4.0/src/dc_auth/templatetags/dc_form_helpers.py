"""
Django template tags/filters to assist with making forms more appealing/use
the bulma framework.
"""
import re

from django import template
from django import forms
from django.utils.safestring import mark_safe

register = template.Library()

# Regex for adding classes to html snippets
class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')

BULMA_INPUT_SUPPORTED_CLASSES = (
    # Classes explicitly supported by bulma (django seems to have no widgets
    # for input type="tel")
    forms.TextInput,
    forms.EmailInput,
    forms.PasswordInput,
    # Other classes which should use bulma input class
    forms.URLInput,
    forms.NumberInput,
)


@register.filter
def add_class(value, css_class):
    """
    Inserts classes into template variables that contain HTML tags,
    useful for modifying forms without needing to change the Form objects.

    Usage:

        {{ field.label_tag|add_class:"control-label" }}

    In this case, the filter is used to add css-framework-specific
    classes to the forms.

    See https://stackoverflow.com/q/4124220/1306020
    """
    # pylint: disable=consider-using-f-string,invalid-name
    html = str(value)
    match = class_re.search(html)
    if match:
        m = re.search(
            r"^%s$|^%s\s|\s%s\s|\s%s$"
            % (css_class, css_class, css_class, css_class),
            match.group(1),
        )
        if not m:
            return mark_safe(
                class_re.sub(match.group(1) + " " + css_class, html)
            )
    else:
        return mark_safe(html.replace(">", ' class="%s">' % css_class, 1))
    return value


@register.filter
def is_textarea(field):
    """
    Django template filter function to check if the field has a HTML textarea
    widget.
    """
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_checkbox(field):
    """
    Django template filter function to check if the field has a HTML checkbox
    widget.
    """
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def can_use_bulma_input(field):
    """
    Django template filter function to check if the field can have the Bulma
    framework input class applied without issue.
    """
    return isinstance(field.field.widget, BULMA_INPUT_SUPPORTED_CLASSES)
