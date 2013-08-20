from django_filters.filterset import filterset_factory
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.core.urlresolvers import reverse


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


class BetterMetaMixin(object):
    '''
    Functions for accessing Meta-data in views.
    #####################################################
    TODO: Functions in this class are clearly duplicated
    of those in the BetterModelAdmin class. This symptoms
    say that probably the code can be better organized.
    #####################################################
    '''
    def get_model(self):
        '''
        Returns model of defined queryset
        '''
        return self.get_queryset().model

    def get_model_name(self):
        '''
        Returns name of the model
        '''
        model = self.get_model()
        return model._meta.object_name

    def get_model_name_plural(self):
        '''
        Returns plural name of the model
        '''
        model = self.get_queryset().model
        return model._meta.verbose_name_plural.title()

    def get_app_name(self):
        '''
        Reutrns the app name that the model for self.queryset belongs to
        '''
        model = self.get_queryset().model
        return model._meta.app_label

    def get_view_name(self, viewtype):
        '''
        Returns a friendly name for our view for use in reverse and the likes.
        '''
        return '%s_%s_%s' % (self.get_app_name().lower(),
                             self.get_model_name().lower(),
                             viewtype)

    def get_list_url(self):
        return reverse(self.get_view_name('list'))

    def get_create_url(self):
        return reverse(self.get_view_name('create'))

    def get_detail_url(self):
        return reverse(self.get_view_name('detail'))

    def get_update_url(self):
        return reverse(self.get_view_name('update'), args=(self.object.pk,))

    def get_delete_url(self):
        return reverse(self.get_view_name('delete'), args=(self.object.pk,))


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
