from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.http import HttpResponse
from django.utils.html import escape
from django.conf import settings


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

    def init_form_from_get(self, form):
        """
        Init form from the parameters in GET querystring.
        """
        for key in self.request.GET:
            try:
                form.fields[key].initial = self.request.GET[key]
                # TODO: Doing this because I do not have the javascript 
                # in my templates to post forms with disabled fields.
                #form.fields[key].widget.attrs['disabled'] = 'disabled'
            except KeyError:
                pass

    def get_form(self, form_class):
        """
        Plug-in the pre_render hook.
        """
        form = form_class(**self.get_form_kwargs())
        if not self.pre_render == None:
            self.pre_render(form, self.request)
        self.init_form_from_get(form)
        return form

    def form_valid(self, form):
        """
        Plug-in the pre_save hook.
        """
        if not self.pre_save == None:
            self.pre_save(form, self.request)
        return super(HookMixin, self).form_valid(form)


class PopupMixin(HookMixin):
    """
    To be used with PopupView. Provides pre-rendering and pre-saving hooks
    via HookMixin and a special form_valid for the popups
    """

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
    # points to a function that dynamically returns querysey using request
    request_queryset = None
    # dictionary for holding miscellany
    extra_context = None

    def get_base_queryset(self):
        """
        This overrides the function by the same name present in 
        ListFilteredMixin. It hooks up the get_request_queryset
        method the is passed in from the admin.
        """
        if not self.request_queryset is None:
            return self.request_queryset(self.request)
        else:
            return super(BaseViewMixin, self).get_base_queryset()

    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        if self.extra_context is None:
            self.extra_context = {}
        context['extra'] = self.extra_context
        return context


class TemplateUtilsMixin(object):
    """
    Functions that answer common questions about model. These questions are
    generally asked by the templates and since the view instance is a part
    of the context that is passed to the template, this is a nice place to
    put these functions. Alternative included template_tags but they seem
    an unnecessary complication at the moment. 
    """
    def get_project_name(self):
        """
        Returns name of the project
        """
        return getattr(settings, 'PROJECT_NAME', 
            'Define PROJECT_NAME in settings.py')

    def get_model_name(self):
        """
        Returns name of the model - For use in templates
        """
        meta = self.get_queryset().model._meta
        return meta.object_name

    def get_model_name_plural(self):
        """
        Returns plural name of the model - For use in templates
        """
        meta = self.get_queryset().model._meta
        return meta.verbose_name_plural

    def get_app_name(self):
        """
        Reutrns the app name that the model for self.queryset
        belongs to - For use in templates
        """
        meta = self.get_queryset().model._meta
        return meta.app_label

    def get_model_fields(self):
        """
        Returns the field names of model - For use in templates
        """
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

class BetterSuccessMessageMixin(SuccessMessageMixin):
    """
    Overrides the get_success_url method in order to preserve querystring
    on post-success redirects.
    """

    def get_success_url(self):
        """
        If request has a querystring, append it to the success_url.
        """
        url = super(BetterSuccessMessageMixin, self).get_success_url()
        q = '&'.join(['%s=%s' % q for q in self.request.GET.iteritems()])
        return url + '?' + q
