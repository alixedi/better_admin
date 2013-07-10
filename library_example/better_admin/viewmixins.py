from enhanced_cbvs.views.list import ListFilteredMixin
from django_filter.filterset import filterset_factory
from django_tables2 import Table, SingleTableMixin


class BetterListFilteredMixin(ListFilteredMixin):
    '''
    We are going to try and generate default FilterSet if none is specified
    using the filter_set property instead of raising an ImproperlyConfigured
    exception.

    Details about ListFilteredMixin can be browsed in the code.
    '''
    def get_filter_set(self):
        if self.filter_set:
            return self.filter_set
        else:
            model = self.get_base_queryset().model
            # django_filter has a filterset_factory
            klass = filterset_factory(model)
            return klass


class BetterSingleTableMixin(SingleTableMixin):
    '''
    We are going to try and generate a default Table is none is specified
    using the table_class property instead of raising an ImproperlyConfigured
    exception.

    Details about SingleTableMixin can be read here:
    http://django-tables2.readthedocs.org/en/latest/#class-based-generic-mixins
    '''
    def get_table_class(self):
        if self.table_class:
            return self.table_class
        else:
            model = self.get_base_queryset().model
            model_name = model._meta.object_name
            # Dynamic class definition using the type recipe
            # http://docs.python.org/2/library/functions.html#type
            klass = type('%sTable' % model_name,
                         (Table,),
                         dict(model=model))
            return klass
