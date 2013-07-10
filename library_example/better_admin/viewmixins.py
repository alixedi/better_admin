from enhanced_cbvs.views.list import ListFilteredMixin
from django_filter.filterset import filterset_factory
from django_tables2 import Table, SingleTableMixin
from django.exception import ImproperlyConfigured


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



# This is not mine. It belongs to django-enhanced-cbvs here:
# https://github.com/rasca/django-enhanced-cbv
# However, the same is not packaged for distribution from
# pip or from tar.gz distributed via GitHub.
class ListFilteredMixin(object):
    """
    Mixin that adds support for django-filter
    """

    filter_set = None
    
    def get_filter_set(self):
        if self.filter_set:
            return self.filter_set
        else:
            raise ImproperlyConfigured(
                "ListFilterMixin requires either a definition of "
                "'filter_set' or an implementation of 'get_filter()'")

    def get_filter_set_kwargs(self):
        """
        Returns the keyword arguments for instanciating the filterset.
        """
        return {
            'data': self.request.GET,
            'queryset': self.get_base_queryset(),
        }

    def get_base_queryset(self):
        """
        We can decided to either alter the queryset before or after applying the
        FilterSet
        """
        return super(ListFilteredMixin, self).get_queryset()

    def get_constructed_filter(self):
        # We need to store the instantiated FilterSet cause we use it in
        # get_queryset and in get_context_data
        if getattr(self, 'constructed_filter', None):
            return self.constructed_filter
        else:
            f = self.get_filter_set()(**self.get_filter_set_kwargs())
            self.constructed_filter = f
            return f

    def get_queryset(self):
        return self.get_constructed_filter().qs

    def get_context_data(self, **kwargs):
        kwargs.update({'filter': self.get_constructed_filter()})
        return super(ListFilteredMixin, self).get_context_data(**kwargs)
