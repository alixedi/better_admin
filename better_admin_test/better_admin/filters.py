from django import forms

from django_filters.filterset import FilterSet
from django_filters.widgets import RangeWidget
from django_filters.filters import Filter, RangeFilter


class CustomMultiValueField(forms.MultiValueField):
    widget = RangeWidget

    def compress(self, data_list):
        if data_list:
            return slice(*data_list)
        return None


class DateRangeField(CustomMultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateField(),
            forms.DateField(),
        )
        super(DateRangeField, self).__init__(fields, *args, **kwargs)


class TimeRangeField(CustomMultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.TimeField(),
            forms.TimeField(),
        )
        super(TimeRangeField, self).__init__(fields, *args, **kwargs)


class DateTimeRangeField(CustomMultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateTimeField(),
            forms.DateTimeField(),
        )
        super(DateTimeRangeField, self).__init__(fields, *args, **kwargs)


class CustomRangeFilter(Filter):
    def filter(self, qs, value):
        if value:
            lookup = '%s__range' % self.name
            return qs.filter(**{lookup: (value.start, value.stop)})
        return qs


class DateRangeFilter(CustomRangeFilter):
    field_class = DateRangeField


class TimeRangeFilter(CustomRangeFilter):
    field_class = TimeRangeField


class DateTimeRangeFilter(CustomRangeFilter):
    field_class = DateTimeRangeField


def filterset_factory(model):
    meta = type(str('Meta'), (object,), {'model': model})
    filterset = type(str('%sFilterSet' % model._meta.object_name),
                     (FilterSet,), {'Meta': meta})

    for field in filterset.base_filters.keys():
        cls_name = filterset.base_filters[field].__class__.__name__
        if cls_name == 'CharFilter':
            filterset.base_filters[field].lookup_type = 'icontains'
        elif cls_name == 'NumberFilter':
            filterset.base_filters[field] = RangeFilter(name=field)
        elif cls_name == 'TimeFilter':
            filterset.base_filters[field] = TimeRangeFilter(name=field)
        elif cls_name == 'DateFilter':
            filterset.base_filters[field] = DateRangeFilter(name=field)
        elif cls_name == 'DateTimeFilter':
            filterset.base_filters[field] = DateTimeRangeFilter(name=field)
    return filterset
