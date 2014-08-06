"""
Filters Factory & custom Filters
"""
from django import forms

from django_filters.filterset import FilterSet
from django_filters.widgets import RangeWidget
from django_filters.filters import Filter, RangeFilter

from better_admin.glob_field import GlobField
from django.db.models import Q


class CustomMultiValueField(forms.MultiValueField):
    """
    Custom MultiValue Field for Range Filters Field
    """
    widget = RangeWidget

    def compress(self, data_list):
        if data_list:
            return slice(*data_list)
        return None

class DateRangeField(CustomMultiValueField):
    """
    Custom Date Range Filter Field
    """
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateField(),
            forms.DateField(),
        )
        super(DateRangeField, self).__init__(fields, *args, **kwargs)


class TimeRangeField(CustomMultiValueField):
    """
    Custom Time Range Filter Field
    """
    def __init__(self, *args, **kwargs):
        fields = (
            forms.TimeField(),
            forms.TimeField(),
        )
        super(TimeRangeField, self).__init__(fields, *args, **kwargs)


class DateTimeRangeField(CustomMultiValueField):
    """
    Custom DateTime Range Filter Field
    """
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateTimeField(),
            forms.DateTimeField(),
        )
        super(DateTimeRangeField, self).__init__(fields, *args, **kwargs)


class DateTimeRangeWidget(forms.MultiWidget):
    """
    Attached widgets with model DateTime Field
    """
    def __init__(self, attrs=None):
        attrs = {}
        attrs['class'] = "input-append date form_datetime"
        widgets = (forms.DateTimeInput(attrs=attrs), forms.DateTimeInput(attrs=attrs))
        super(DateTimeRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def format_output(self, rendered_widgets):
        return '-'.join(rendered_widgets)


class CustomDateTimeMultiValueField(forms.MultiValueField):
    """
    Custom MultiValue Field for Range Filters Field.
    customized widget added here i.e DateTimeRangeWidget
    """
    widget = DateTimeRangeWidget

    def compress(self, data_list):
        if data_list:
            return slice(*data_list)
        return None


class CustomDateTimeRangeField(CustomDateTimeMultiValueField):
    """
    Custom DateTime Range Filter Field
    """
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateTimeField(),
            forms.DateTimeField(),
        )
        super(CustomDateTimeRangeField, self).__init__(fields, *args, **kwargs)


class EffectiveDateTimeFilter(Filter):
    """
    Custom EffectiveDateTimeFilter to filter records from activation till
    expiration date
    """
    field_class = CustomDateTimeRangeField
    def filter(self, qs, value):
        if value:
            try:
                qs = qs.filter(Q(activation_date__lte=value.stop),
                               Q(expiration_date__gte=value.start) |
                               Q(expiration_date=None))
            except Exception as ex:
                print 'Exception in EffectiveDateTimeFilter: ', ex
                qs = qs.model.objects.none()
        return qs


class WildCardFilter(Filter):
    """
    WildCard Filter to Support Wild Card Like ? * in search
    """
    field_class = GlobField

    def filter(self, qs, value):
        if value:
            lookup = '%s__iregex' % self.name
            try:
                qs = qs.filter(**{lookup: value})
            except Exception as ex:
                print 'Exception in Wild Card Filter: ', ex
                qs = qs.model.objects.none()
        return qs


class CustomRangeFilter(Filter):
    """
    Custom Range Filter
    """
    def filter(self, qs, value):
        if value:
            lookup = '%s__range' % self.name
            return qs.filter(**{lookup: (value.start, value.stop)})
        return qs


class DateRangeFilter(CustomRangeFilter):
    """
    Custom Date Range Filter
    """
    field_class = DateRangeField


class TimeRangeFilter(CustomRangeFilter):
    """
    Custom Time Range Filter
    """
    field_class = TimeRangeField


class DateTimeRangeFilter(CustomRangeFilter):
    """
    Custom DateTime Range Filter
    """
    field_class = DateTimeRangeField


def filterset_factory(model):
    """
    Update Filters by Fields Type
    """
    meta = type(str('Meta'), (object,), {'model': model})
    filterset = type(str('%sFilterSet' % model._meta.object_name),
                     (FilterSet,), {'Meta': meta})

    for field in filterset.base_filters.keys():
        cls_name = filterset.base_filters[field].__class__.__name__
        if cls_name == 'CharFilter':
            filterset.base_filters[field] = WildCardFilter(name=field)
        elif cls_name == 'NumberFilter':
            filterset.base_filters[field] = RangeFilter(name=field)
        elif cls_name == 'TimeFilter':
            filterset.base_filters[field] = TimeRangeFilter(name=field)
        elif cls_name == 'DateFilter':
            filterset.base_filters[field] = DateRangeFilter(name=field)
        elif cls_name == 'DateTimeFilter':
            filterset.base_filters[field] = DateTimeRangeFilter(name=field)
    return filterset
