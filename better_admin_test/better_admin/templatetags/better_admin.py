from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings


register = template.Library()

@register.simple_tag
def get_project_name():
    """
    Returns the project name as defined 
    """
    return getattr(settings, 'PROJECT_NAME', 
                             'Define PROJECT_NAME in settings.py')

@register.filter
def get_field_value(obj, field_name):
    """
    Returns value for the given field for a given object.
    Fields here refer to field of object. To be used in 
    ListView.
    """
    return getattr(obj, field_name, None)

@register.filter
def get_field_type(field):
    """
    Returns type for the given field. Fields here refer to 
    field of object. To be used in 
    ListView.
    """
    type_str = str(type(field))
    type_str = type_str.lstrip('\'<')
    type_str = type_str.rstrip('\'>')
    return type_str.split('.')[-1]

@register.filter
def get_form_field_type(field):
    """
    Returns value for the given field for a form. To be used
    in CreateView and UpdateView.
    """
    return field.field.__class__.__name__

@register.filter(is_safe=True, needs_autoescape=True)
def get_fk_link(field, obj, autoescape=None):
    """
    Returns link to FK. Used in ListView to put in links for
    ForeignKey fields. Field here refer to field of object.
    """
    model = field.rel.to
    model_name = model._meta.object_name.lower()
    app_name = model._meta.app_label.lower()
    view_name = '%s_%s_%s' % (app_name, model_name, 'detail')
    field_value = getattr(obj, field.name, None)
    try:
        href = reverse(view_name, args=(field_value.pk,))
        return mark_safe("<a href='%s'>%s</a>" % (href, field_value))
    except:
        return mark_safe("%s" % field_value)

@register.filter
def get_fk_popup_url(field):
    """
    Returns url of the popup for the given ForeignKey field. The
    link follows the better_admin url conventions. To be used in 
    CreateView and UpdateView for putting a + against every 
    ForeignKey field.
    """
    model = field.field.queryset.model
    model_name = model._meta.object_name.lower()
    app_name = model._meta.app_label.lower()
    return '%s/%s/popup' % (app_name, model_name)
