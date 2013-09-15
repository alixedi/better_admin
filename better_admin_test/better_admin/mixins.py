from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, url
from django.core.exceptions import ImproperlyConfigured

from django_filters.filterset import filterset_factory
from import_export.admin import ImportExportMixin
from import_export.resources import modelresource_factory

from better_admin.views import BetterListView, BetterDetailView, \
                               BetterCreateView, BetterUpdateView, \
                               BetterDeleteView, BetterPopupView


class BetterListAdminMixin(object):
    """
    Creates and takes care of ListView
    """

    list_view = None
    list_perm = None
    list_template = None
    filter_set = None
    actions = None

    def get_list_perm(self):
        """
        Returns the given list perm or default
        """
        if not self.list_perm is None:
            return self.list_perm
        else:
            meta = self.get_model()._meta
            info = meta.app_label, meta.object_name
            return '%s.view_%s' % info

    def get_list_template(self):
        """
        Returns the given list template or default
        """
        if not self.list_template is None:
            return self.list_template
        else:
            return 'better_admin/list.html'

    def get_filter_set(self):
        """
        Returns given filte_rset or default
        """
        if not self.filter_set is None:
            return self.filter_set
        else:
            # TODO: filterset factory
            model = self.get_model()
            return filterset_factory(model)

    def get_actions(self):
        """
        Returns given actions or default
        """
        if not self.actions is None:
            return self.actions
        else:
            # TODO: actions factory
            return []

    def get_list_view(self):
        """
        Returns a list view 
        """
        if not self.list_view is None:
            return self.list_view
        else:
            model = self.get_model()
            queryset = self.get_queryset()
            request_queryset = self.get_request_queryset
            name = '%sListView' % model._meta.object_name
            perm = self.get_list_perm()
            temp = self.get_list_template()
            filter_set = self.get_filter_set()
            actions = self.get_actions()

            return type(name,
                        (BetterListView,),
                        dict(model=model,
                             queryset=queryset,
                             request_queryset = request_queryset,
                             permission_required=perm,
                             template_name=temp,
                             filter_set=filter_set,
                             actions=actions))

    def get_list_urls(self):
        """
        Returns URLs for list view
        """
        meta = self.get_model()._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_list' % info
        list_view = self.get_list_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/$' % base_url,
                            list_view.as_view(),
                            name=view_name))


class BetterDetailAdminMixin(object):
    """
    Creates and takes care of a DetailView
    Requires the definition of get_queryset()
    """

    detail_view = None
    detail_perm = None
    detail_template = None

    def get_detail_perm(self):
        """
        Returns the given perm or default
        """
        if not self.detail_perm is None:
            return self.detail_perm
        else:
            meta = self.get_model()._meta
            info = meta.app_label, meta.object_name
            return '%s.view_%s' % info

    def get_detail_template(self):
        """
        Returns the given template or default
        """
        if not self.detail_template is None:
            return self.detail_template
        else:
            return 'better_admin/detail.html'

    def get_detail_view(self):
        """
        Returns a detail view 
        """
        if not self.detail_view is None:
            return self.detail_view
        else:
            model = self.get_model()
            queryset = self.get_queryset()
            request_queryset = self.get_request_queryset
            name = '%sDetailView' % model._meta.object_name
            perm = self.get_detail_perm()
            temp = self.get_detail_template()

            return type(name,
                        (BetterDetailView,),
                        dict(model=model,
                             queryset=queryset,
                             request_queryset=request_queryset,
                             permission_required=perm,
                             template_name=temp))

    def get_detail_urls(self):
        """
        Returns URLs for detail view
        """
        meta = self.get_model()._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_detail' % info
        detail_view = self.get_detail_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/(?P<pk>[a-zA-Z0-9_]+)/$' % base_url,
                            detail_view.as_view(),
                            name=view_name))


class BetterCreateAdminMixin(object):
    """
    Creates and takes care of a CreateView
    Requires the definition of get_queryset()
    """
    create_view = None
    create_perm = None
    create_form = None
    create_template = None
    create_success_url = None
    create_success_message = None

    def get_create_perm(self):
        """
        Returns the given perm or default
        """
        if not self.create_perm is None:
            return self.create_perm
        else:
            meta = self.get_model()._meta
            info = meta.app_label.lower(), meta.object_name.lower()
            return '%s.add_%s' % info

    def get_create_template(self):
        """
        Returns the given template or default
        """
        if not self.create_template is None:
            return self.create_template
        else:
            return 'better_admin/create.html'

    def get_create_form(self):
        """
        Returns the given form class or None
        """
        if not self.create_form is None:
            return self.create_form
        else:
            # TODO: Intelligent Form Factory?
            return None

    def get_create_success_url(self):
        """
        Returns the given success url or default
        """
        if not self.create_success_url is None:
            return self.create_success_url
        else:
            meta = self.get_model()._meta
            info = meta.app_label.lower(), meta.object_name.lower()
            view_name = '%s_%s_list' % info
            return reverse_lazy(view_name)

    def get_create_success_message(self):
        """
        Returns the given success message or default
        """
        if not self.create_success_message is None:
            return self.create_success_message
        else:
            meta = self.get_model()._meta
            return '%s was created successfully' % meta.object_name 

    def create_pre_render(self, form, request):
        """
        This function will be passed to the CreateView and will be executed
        just before the form is rendered. You may over-ride this and code
        useful logic such as removing and/or pre-setting fields.
        """
        pass

    def create_pre_save(self, form, request):
        """
        This function will be passed to the CreateView and will be executed
        after validation and just before the form is saved. You may over-ride
        this and code useful logic such as removing and/or pre-setting fields.
        """
        pass

    def get_create_view(self):
        """
        Returns a create view 
        """
        if not self.create_view is None:
            return self.create_view
        else:
            model = self.get_model()
            queryset = self.get_queryset()
            request_queryset = self.get_request_queryset
            name = '%sCreateView' % model._meta.object_name
            perm = self.get_create_perm()
            temp = self.get_create_template()
            form = self.get_create_form()
            suc_url = self.get_create_success_url()
            suc_msg = self.get_create_success_message()

            return type(name,
                        (BetterCreateView,),
                        dict(queryset=queryset,
                             request_queryset=request_queryset,
                             permission_required=perm,
                             template_name=temp,
                             form_class=form,
                             success_url=suc_url,
                             success_message=suc_msg,
                             pre_render=self.create_pre_render,
                             pre_save=self.create_pre_save))

    def get_create_urls(self):
        """
        Returns URLs for create view
        """
        meta = self.get_model()._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_create' % info
        create_view = self.get_create_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/create/$' % base_url,
                            create_view.as_view(),
                            name=view_name))


class BetterPopupAdminMixin(object):
    """
    Creates and takes care of a PopupView
    Requires the definition of get_queryset()
    """
    popup_view = None
    popup_perm = None
    popup_form = None
    popup_template = None

    def get_popup_perm(self):
        """
        Returns the given perm or default
        """
        if not self.popup_perm is None:
            return self.popup_perm
        else:
            meta = self.get_model()._meta
            info = meta.app_label.lower(), meta.object_name.lower()
            return '%s.add_%s' % info

    def get_popup_template(self):
        """
        Returns the given template or default
        """
        if not self.popup_template is None:
            return self.popup_template
        else:
            return 'better_admin/popup.html'

    def get_popup_form(self):
        """
        Returns the given form class or None
        """
        if not self.popup_form is None:
            return self.popup_form
        else:
            # TODO: Intelligent Form Factory?
            return None

    def popup_pre_render(self, form, request):
        """
        This function will be passed to the PopupView and will be executed
        just before the form is rendered. You may over-ride this and code
        useful logic such as removing and/or pre-setting fields.
        """
        pass

    def popup_pre_save(self, form, request):
        """
        This function will be passed to the PopupView and will be executed
        after validation and just before the form is saved. You may over-ride
        this and code useful logic such as removing and/or pre-setting fields.
        """
        pass

    def get_popup_view(self):
        """
        Returns a popup view 
        """
        if not self.popup_view is None:
            return self.popup_view
        else:
            model = self.get_model()
            queryset = self.get_queryset()
            request_queryset = self.get_request_queryset
            name = '%sPopupView' % model._meta.object_name
            perm = self.get_popup_perm()
            temp = self.get_popup_template()
            form = self.get_popup_form()

            return type(name,
                        (BetterPopupView,),
                        dict(queryset=queryset,
                             request_queryset=request_queryset,
                             permission_required=perm,
                             template_name=temp,
                             form_class=form,
                             pre_render=self.popup_pre_render,
                             pre_save=self.popup_pre_save))

    def get_popup_urls(self):
        """
        Returns URLs for popup view
        """
        meta = self.get_model()._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_popup' % info
        popup_view = self.get_popup_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/popup/$' % base_url,
                            popup_view.as_view(),
                            name=view_name))


class BetterUpdateAdminMixin(object):
    """
    Creates and takes care of a UpdateView
    Requires the definition of get_queryset()
    """
    update_view = None
    update_perm = None
    update_form = None
    update_template = None
    update_success_url = None
    update_success_message = None

    def get_update_perm(self):
        """
        Returns the given perm or default
        """
        if not self.update_perm is None:
            return self.update_perm
        else:
            meta = self.get_model()._meta
            info = meta.app_label.lower(), meta.object_name.lower()
            return '%s.add_%s' % info

    def get_update_template(self):
        """
        Returns the given template or default
        """
        if not self.update_template is None:
            return self.update_template
        else:
            return 'better_admin/update.html'

    def get_update_form(self):
        """
        Returns the given form class or None
        """
        if not self.update_form is None:
            return self.update_form
        else:
            # TODO: Intelligent Form Factory?
            return None

    def get_update_success_url(self):
        """
        Returns the given success url or default
        """
        if not self.update_success_url is None:
            return self.update_success_url
        else:
            meta = self.get_model()._meta
            info = meta.app_label.lower(), meta.object_name.lower()
            view_name = '%s_%s_list' % info
            return reverse_lazy(view_name)

    def get_update_success_message(self):
        """
        Returns the given success message or default
        """
        if not self.update_success_message is None:
            return self.update_success_message
        else:
            meta = self.get_model()._meta
            return '%s was updated successfully' % meta.object_name 

    def update_pre_render(self, form, request):
        """
        This function will be passed to the UpdateView and will be executed
        just before the form is rendered. You may over-ride this and code
        useful logic such as removing and/or pre-setting fields.
        """
        pass

    def update_pre_save(self, form, request):
        """
        This function will be passed to the UpdateView and will be executed
        after validation and just before the form is saved. You may over-ride
        this and code useful logic such as removing and/or pre-setting fields.
        """
        pass

    def get_update_view(self):
        """
        Returns a update view 
        """
        if not self.update_view is None:
            return self.update_view
        else:
            model = self.get_model()
            queryset = self.get_queryset()
            request_queryset = self.get_request_queryset
            name = '%sUpdateView' % model._meta.object_name
            perm = self.get_update_perm()
            temp = self.get_update_template()
            form = self.get_update_form()
            suc_url = self.get_update_success_url()
            suc_msg = self.get_create_success_message()

            return type(name,
                        (BetterUpdateView,),
                        dict(queryset=queryset,
                             request_queryset=request_queryset,
                             permission_required=perm,
                             template_name=temp,
                             form_class=form,
                             success_url=suc_url,
                             success_message=suc_msg,
                             pre_render=self.update_pre_render,
                             pre_save=self.update_pre_save))

    def get_update_urls(self):
        """
        Returns URLs for update view
        """
        meta = self.get_model()._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_update' % info
        update_view = self.get_update_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/(?P<pk>[a-zA-Z0-9_]+)/update/$' % base_url,
                            update_view.as_view(),
                            name=view_name))


class BetterDeleteAdminMixin(object):
    """
    Creates and takes care of a DeleteView
    Requires the definition of get_queryset()
    """

    delete_view = None
    delete_perm = None
    delete_form = None
    delete_template = None
    delete_success_url = None
    delete_success_message = None

    def get_delete_perm(self):
        """
        Returns the given perm or default
        """
        if not self.delete_perm is None:
            return self.delete_perm
        else:
            meta = self.get_model()._meta
            info = meta.app_label.lower(), meta.object_name.lower()
            return '%s.remove_%s' % info

    def get_delete_template(self):
        """
        Returns the given template or default
        """
        if not self.delete_template is None:
            return self.delete_template
        else:
            return 'better_admin/delete.html'

    def get_delete_form(self):
        """
        Returns the given form class or None
        """
        if not self.delete_form is None:
            return self.delete_form
        else:
            # TODO: Intelligent Form Factory?
            return None

    def get_delete_success_url(self):
        """
        Returns the given success url or default
        """
        if not self.delete_success_url is None:
            return self.delete_success_url
        else:
            meta = self.get_model()._meta
            info = meta.app_label.lower(), meta.object_name.lower()
            view_name = '%s_%s_list' % info
            return reverse_lazy(view_name)

    def get_delete_success_message(self):
        """
        Returns the given success message or default
        """
        if not self.delete_success_message is None:
            return self.delete_success_message
        else:
            meta = self.get_model()._meta
            return '%s was deleted successfully' % meta.object_name 

    def delete_pre_render(self, form, request):
        """
        This function will be passed to the DeleteView and will be executed
        just before the form is rendered. You may over-ride this and code
        useful logic such as removing and/or pre-setting fields.
        """
        pass

    def delete_pre_save(self, form, request):
        """
        This function will be passed to the DeleteView and will be executed
        after validation and just before the form is saved. You may over-ride
        this and code useful logic such as removing and/or pre-setting fields.
        """
        pass

    def get_delete_view(self):
        """
        Returns a delete view 
        """
        if not self.delete_view is None:
            return self.delete_view
        else:
            model = self.get_model()
            queryset = self.get_queryset()
            request_queryset = self.get_request_queryset
            name = '%sDeleteView' % model._meta.object_name
            perm = self.get_delete_perm()
            temp = self.get_delete_template()
            form = self.get_delete_form()
            suc_url = self.get_delete_success_url()
            suc_msg = self.get_delete_success_message()

            return type(name,
                        (BetterDeleteView,),
                        dict(queryset=queryset,
                             request_queryset=request_queryset,
                             permission_required=perm,
                             template_name=temp,
                             form_class=form,
                             success_url=suc_url,
                             success_message=suc_msg,
                             pre_render=self.delete_pre_render,
                             pre_save=self.delete_pre_save))

    def get_delete_urls(self):
        """
        Returns URLs for delete view
        """
        meta = self.get_model()._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_delete' % info
        delete_view = self.get_delete_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/(?P<pk>[a-zA-Z0-9_]+)/delete/$' % base_url,
                            delete_view.as_view(),
                            name=view_name))


import tempfile
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from import_export.forms import ExportForm, ConfirmImportForm, ImportForm
from import_export.formats import base_formats

#: import / export formats
DEFAULT_FORMATS = (
    base_formats.CSV,
    base_formats.XLS,
    base_formats.TSV,
    base_formats.ODS,
    base_formats.JSON,
    base_formats.YAML,
    base_formats.HTML,
)


class BetterImportAdminMixin(object):
    """
    Create and takes care of ImportView for importing data using 
    django-import-export.
    """

    #: template for import view
    import_template_name = 'import_export/import.html'
    #: resource class
    import_resource = None
    #: available import formats
    formats = DEFAULT_FORMATS
    #: import data encoding
    from_encoding = "utf-8"

    def get_import_resource(self):
        """
        Returns self.import_resource or default
        """
        if not self.import_resource is None:
            return self.import_resource
        else:
            model = self.get_model()
            return modelresource_factory(model)

    def get_import_urls(self):
        """
        Returns import urls.
        """
        meta = self.get_model()._meta
        info = meta.app_label, meta.module_name
        base_url = '%s/%s' % info
        view_name = '%s_%s_delete' % info

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/process_import/$' % base_url,
                            self.process_import,
                            name=view_name),
                        url(r'^%s/import/$' % base_url,
                            self.import_action,
                            name=view_name))

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def process_import(self, request, *args, **kwargs):
        '''
        Perform the actuall import action (after the user has confirmed he
        wishes to import)
        '''
        opts = self.get_model()._meta
        resource = self.get_import_resource()()

        confirm_form = ConfirmImportForm(request.POST)
        if confirm_form.is_valid():
            import_formats = self.get_import_formats()
            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            import_file = open(confirm_form.cleaned_data['import_file_name'],
                               input_format.get_read_mode())
            data = import_file.read()
            if not input_format.is_binary() and self.from_encoding:
                data = unicode(data, self.from_encoding).encode('utf-8')
            dataset = input_format.create_dataset(data)

            resource.import_data(dataset, dry_run=False,
                                 raise_errors=True)

            success_message = 'Import finished'
            messages.success(request, success_message)
            import_file.close()

            url = reverse('%s_%s_list' %
                          (opts.app_label.lower(), opts.object_name.lower()))
            return HttpResponseRedirect(url)

    def import_action(self, request, *args, **kwargs):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          request.POST or None,
                          request.FILES or None)

        if request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
                for chunk in import_file.chunks():
                    uploaded_file.write(chunk)

            # then read the file, using the proper format-specific mode
            with open(uploaded_file.name,
                      input_format.get_read_mode()) as uploaded_import_file:
                # warning, big files may exceed memory
                data = uploaded_import_file.read()
                if not input_format.is_binary() and self.from_encoding:
                    data = unicode(data, self.from_encoding).encode('utf-8')
                dataset = input_format.create_dataset(data)
                result = resource.import_data(dataset, dry_run=True,
                                              raise_errors=False)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': uploaded_file.name,
                    'input_format': form.cleaned_data['input_format'],
                })

        context['form'] = form
        context['opts'] = self.get_model()._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(request, [self.import_template_name], context)



class BetterExportAdminMixin(object):
    """
    Create and takes care of ExportView for exporting data using 
    django-import-export.
    """
    #: resource class
    export_resource = None
    #: template for export view
    export_template_name = 'import_export/export.html'
    #: available import formats
    formats = DEFAULT_FORMATS
    #: export data encoding
    to_encoding = "utf-8"

    def get_export_resource(self):
        """
        Returns self.export_resource or default
        """
        if not self.export_resource is None:
            return self.export_resource
        else:
            model = self.get_model()
            return modelresource_factory(model)

    def get_export_urls(self):
        """
        Returns export urls.
        """
        meta = self.get_model()._meta
        info = meta.app_label, meta.module_name
        base_url = '%s/%s' % info
        view_name = '%s_%s_delete' % info

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/export/$' % base_url,
                            self.export_action,
                            name=view_name))

    def get_export_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_export()]

    def get_export_filename(self, file_format):
        """
        Come up with a reasonable file name for the export
        """
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s.%s" % (self.get_model().__name__,
                                 date_str,
                                 file_format.get_extension())
        return filename

    def export_action(self, request, *args, **kwargs):
        """
        The function based view that does the export. Copied from 
        import_export/resouces.py - the original could not work 
        because of references to admin.
        """
        formats = self.get_export_formats()
        form = ExportForm(formats, request.POST or None)
        if form.is_valid():
            file_format = formats[
                int(form.cleaned_data['file_format'])
            ]()

            resource_class = self.get_export_resource()
            queryset = self.get_request_queryset(request)
            data = resource_class().export(queryset)
            response = HttpResponse(
                file_format.export_data(data),
                mimetype='application/octet-stream',
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % (
                self.get_export_filename(file_format),
            )
            return response

        context = {}
        context['form'] = form
        context['opts'] = self.get_model()._meta
        return TemplateResponse(request, [self.export_template_name], context)


class BetterModelAdminMixin(object):
    """
    Generic functions that are required by Better<view_type>AdminMixins
    to work.
    """

    model = None
    queryset = None

    def get_model(self):
        """
        Returns self.model, self.queryset.model or raises an exception.
        """
        if not self.model is None:
            return self.model
        else:
            if not self.queryset is None:
                return self.queryset.model
            else:
                raise ImproperlyConfigured(("BetterModelAdmin requires a "
                                            "definition of model or queryset "
                                            "property."))

    def get_queryset(self):
        """
        This method is passed to the respective View where it is plugged into
        the get_queryset method. You can over-ride this to put in logic that
        generates the queryset dynamically based on request. For instance, 
        only showing contacts that are friends with request.user
        By default, it returns self.queryset, self.model.objects.all() or 
        raises an exception.
        """
        if not self.queryset is None:
            return self.queryset
        else:
            if not self.model is None:
                return self.model.objects.all()
            else:
                raise ImproperlyConfigured(("BetterModelAdmin requires a "
                                            "definition of model or queryset "
                                            "property."))

    def get_request_queryset(self, request):
        """
        This method is passed to the respective View where it is plugged into
        the get_queryset method. You can over-ride this to put in logic that
        generates the queryset dynamically based on request. For instance, 
        only showing contacts that are friends with request.user
        """
        return self.get_queryset()


class ReadOnlyModelAdminMixin(BetterListAdminMixin,
                              BetterDetailAdminMixin,
                              BetterModelAdminMixin):
    """
    Read-only support. Does not support editing.
    """
    pass


class CreateOnlyModelAdminMixin(BetterListAdminMixin,
                                BetterDetailAdminMixin,
                                BetterCreateAdminMixin,
                                BetterPopupAdminMixin,
                                BetterModelAdminMixin):
    """
    Create-onle support. Does not include editing or deleting.
    """
    pass


class CreateAndUpdateModelAdminMixin(BetterListAdminMixin,
                                     BetterDetailAdminMixin,
                                     BetterCreateAdminMixin,
                                     BetterPopupAdminMixin,
                                     BetterModelAdminMixin):
    """
    Create-onle support. Does not include editing or deleting.
    """
    pass


class BetterModelAdminMixin(BetterListAdminMixin,
                            BetterDetailAdminMixin,
                            BetterCreateAdminMixin,
                            BetterUpdateAdminMixin,
                            BetterDeleteAdminMixin,
                            BetterPopupAdminMixin,
                            BetterExportAdminMixin,
                            BetterImportAdminMixin,
                            BetterModelAdminMixin):
    """
    Complete CRUD support.
    """
    pass