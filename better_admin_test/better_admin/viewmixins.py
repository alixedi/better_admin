from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.http import HttpResponse
from django.utils.html import escape


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


class HookMixin(object):
    """
    To be used with CBVs derived from FormView. Provides pre-rendering and
    pre-saving hooks for inserting useful logic. 
    """
    pre_render = None
    pre_save = None

    def get_form(self, form_class):
        """
        Plug-in the pre_render hook.
        """
        form = form_class(**self.get_form_kwargs())
        if not self.pre_render == None:
            self.pre_render(form, self.request)
        return form

    def form_valid(self, form):
        """
        Plug-in the pre_save hook.
        """
        if not self.pre_save == None:
            self.pre_save(form, self.request)
        return super(HookMixin, self).form_valid(form)


class PopupMixin(object):
    """
    To be used with PopupView. Provides pre-rendering and pre-saving hooks
    for inserting useful logic a la HookMixin
    """
    pre_render = None
    pre_save = None

    def get_form(self, form_class):
        """
        Plug-in the pre_render hook.
        """
        form = form_class(**self.get_form_kwargs())
        if not self.pre_render == None:
            self.pre_render(form, self.request)
        return form


    def form_valid(self, form):
        """
        Plug-in the pre_render hook plus the special popup response
        that closes the popup.
        """
        if not self.pre_save == None:
            self.pre_save(form, self.request)
        new_obj = form.save()
        return HttpResponse("""
            <script type="text/javascript">
                opener.dismissAddAnotherPopup(window, "%s", "%s");
                $('.selectpicker').selectpicker('render');
            </script>""" % (escape(new_obj._get_pk_val()), escape(new_obj)))


class BaseViewMixin(object):
    """
    Functions that are a part of every view. At the moment, this include
    over-riding the get_queryset function to include the request_queryset
    hook.
    """

    request_queryset = None

    def get_base_queryset(self):
        if not self.request_queryset is None:
            return self.request_queryset(self.request)
        else:
            return super(BaseViewMixin, self).get_queryset()


class TemplateUtilsMixin(object):
    """
    Functions that answer common questions about model. These questions are
    generally asked by the templates and since the view instance is a part
    of the context that is passed to the template, this is a nice place to
    put these functions. Alternative included template_tags but they seem
    an unnecessary complication at the moment. 
    """
    def get_model_name(self):
        '''
        Returns name of the model - For use in templates
        '''
        meta = self.get_queryset().model._meta
        return meta.object_name

    def get_model_name_plural(self):
        '''
        Returns plural name of the model - For use in templates
        '''
        meta = self.get_queryset().model._meta
        return meta.verbose_name_plural

    def get_app_name(self):
        '''
        Reutrns the app name that the model for self.queryset
        belongs to - For use in templates
        '''
        meta = self.get_queryset().model._meta
        return meta.app_label

    def get_model_fields(self):
        '''
        Returns the field names of model - For use in templates
        '''
        meta = self.get_queryset().model._meta
        return meta.fields


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
