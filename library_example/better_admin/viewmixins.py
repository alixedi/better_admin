from django_filters.filterset import filterset_factory
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages


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
        We can decided to either alter the queryset before or after applying
        the FilterSet
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


# Backported from Django 1.6
# https://github.com/django/django/blob/master/django/contrib/messages/views.py
class SuccessMessageMixin(object):
    """
    Adds a success message on successful form submission.
    """
    success_message = ''

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data
