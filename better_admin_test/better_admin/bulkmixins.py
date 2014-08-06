"""
TODO: Eerything in this file is a dirty hack from django-import-export's
admin mixins that were originally intended to be used with django-admin.
We have been able to turn them around but this is not tested and may break
so use with care.
"""

import tempfile
from datetime import datetime

from django.conf.urls import patterns, url
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from import_export.resources import modelresource_factory
from import_export.forms import ExportForm, ConfirmImportForm, ImportForm
from import_export.formats import base_formats
from better_admin.import_export_extras import CustomXLS


#: import / export formats
DEFAULT_FORMATS = (
    base_formats.CSV,
    CustomXLS,
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
        view_name1 = '%s_%s_process_import' % info
        view_name2 = '%s_%s_import' % info

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/process_import/$' % base_url,
                            self.process_import,
                            name=view_name1),
                        url(r'^%s/import/$' % base_url,
                            self.import_action,
                            name=view_name2))

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    @user_passes_test(lambda u: u.is_superuser)
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

    @user_passes_test(lambda u: u.is_superuser)
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
        view_name = '%s_%s_export' % info

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

    @user_passes_test(lambda u: u.is_superuser)
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
            #Export filtered queryset
            filter_set = self.get_filter_set()
            filtered_queryset = filter_set(request.GET, queryset=self.queryset)
            data = resource.export(filtered_queryset.qs)
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
