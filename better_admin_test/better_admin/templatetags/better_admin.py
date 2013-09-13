from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


register = template.Library()


@register.filter
def get_field_value(obj, field_name):
	'''
	Returns value for the given field for a given object
	'''
	return getattr(obj, field_name, None)


@register.filter
def get_form_field_type(field):
	'''
	Returns value for the given field for a given object
	'''
	return field.field.__class__.__name__


@register.filter
def get_field_type(field):
	'''
	Returns type for the given field
	'''
	type_str = str(type(field))
	type_str = type_str.lstrip('\'<')
	type_str = type_str.rstrip('\'>')
	return type_str.split('.')[-1]


@register.filter(is_safe=True, needs_autoescape=True)
def tagify(values, autoescape=None):
	'''
	Returns tagified values
	'''
	tokens = values.split(',')
	tags = ["<span class='label'>%s</span>" % t for t in tokens]
	html = '\n'.join(tags)
	return mark_safe(html)


@register.filter(is_safe=True, needs_autoescape=True)
def fklink(field, obj, autoescape=None):
	'''
	Returns link to FK
	'''
	model = field.rel.to
	model_name = model._meta.object_name.lower()
	app_name = model._meta.app_label.lower()
	view_name = '%s_%s_%s' % (app_name, model_name, 'detail')
	field_value = getattr(obj, field.name, None)
	try:
		href = reverse(view_name, args=(obj.pk,))
		return mark_safe("<a href='%s'>%s</a>" % (href, field_value))
	except:
		return mark_safe("%s" % field_value)


@register.filter
def get_fk_popup_url(field):
	'''
	Returns url of the popup form for the model of the 
	given foreign-key field
	'''
	model = field.field.queryset.model
	model_name = model._meta.object_name.lower()
	app_name = model._meta.app_label.lower()
	return '%s/%s/popup' % (app_name, model_name)

@register.filter
def get_fk_field_model_name(field):
	'''
	Returns model of the given foreign-key field
	'''
	model = field.field.queryset.model
	model_name = model._meta.object_name
	# TODO: Extend tek-extensions to include app_name in the view
	# kwargs so that conflicting model names can be managed!
	#app_name = model._meta.app_label.lower()
	return model_name