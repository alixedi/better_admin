import django_filters

"""
Lookp types wrt filter type
'CharFilter'
    'contains', 'icontains', 
    'exact', 'iexact', 
    'endswith', 'iendswith', 
    'regex', 'iregex', 
    'search', 
    'startswith', 'istartswith'
'DateFilter'
'DateTimeFilter'
'DateRangeFilter'
'TimeFilter'
'ModelChoiceFilter'
    *take care of queryset contraints*
'ModelMultipleChoiceFilter'
    *take care of queryset contraints*
'NumberFilter'
'RangeFilter'
'AllValuesFilter',
"""

class BetterFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(BetterFilterSet, self).__init__(*args, **kwargs)
        for name, field in self.filters.iteritems():
            if type(field) == django_filters.filters.CharFilter:
                self.filters[name].lookup_type = ['icontains', 'iexact', 'search', 'iregex', 'istartswith', 'iendswith']

def filterset_factory(model):
    meta = type(str('Meta'), (object,), {'model': model})
    filterset = type(str('%sFilterSet' % model._meta.object_name),
                        (BetterFilterSet,), {'Meta': meta})
    return filterset