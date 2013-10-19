from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app, get_models
from django.conf.urls import patterns

from django_nav import Nav, NavOption

from better_admin.adminmixins import BetterModelAdminMixin


class BetterModelAdmin(BetterModelAdminMixin):
    """
    BetterModelAdminMixin creates and takes care of CRUD for the
    givem model.
    """

    def __init__(self):
        """
        Run the factories.
        """
        if self.list_view is None:
            self.list_view = self.get_list_view()
        if self.detail_view is None:
            self.detail_view = self.get_detail_view()
        if self.create_view is None:
            self.create_view = self.get_create_view()
        if self.update_view is None:
            self.update_view = self.get_update_view()
        if self.delete_view is None:
            self.delete_view = self.get_delete_view()
        if self.popup_view is None:
            self.popup_view = self.get_popup_view()
        if self.import_resource is None:
            self.import_resource = self.get_import_resource()
        if self.export_resource is None:
            self.export_resource = self.get_export_resource()

    def get_nav(self):
        """
        Returns subclass of NavOption that points to the ListView of the model.
        """
        meta = self.get_model()._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        view_name = '%s_%s_list' % info
        return type('%sNavOption' % meta.object_name,
                    (NavOption,),
                    dict(name=meta.verbose_name_plural.title(),
                         view=view_name))

    def get_urls(self):
        """
        Gets url patterns in order
        TODO: Use super call to get all urls compiled. Will have to rename
        get_<view_type>_urls to get_urls in all the mixins.
        """
        meta = self.get_model()._meta
        urls = patterns('%s.views' % meta.app_label)
        urls += self.get_create_urls()
        urls += self.get_popup_urls()
        urls += self.get_export_urls()
        urls += self.get_import_urls()
        urls += self.get_update_urls()
        urls += self.get_delete_urls()
        urls += self.get_detail_urls()
        urls += self.get_list_urls()
        return urls


class BetterAppAdmin(object):
    """
    Given a django app, this basically introspects the app, extracts all the
    models and then goes on to create BetterModelAdmins with reasonable
    defaults for each of the model. Moreover, if you want to do something
    special for the BetterModelAdmin of one of the models, this allows you
    to bring your own class and override the defaults. Notice that if you
    want, you may override with a None in order to not have any admin for
    the model of your choice.
    """
    # This is necessary
    app_name = None

    # TODO: This does not work! model_admins becomes a class-level property 
    # and carries the value of the last instantiated object forward. This is
    # not a bug but a documented feature of Python - for immutable types.
    # See here: http://docs.python.org/tutorial/classes.html
    # model_admins = {}

    model_admins = None

    def __init__(self):
        """
        Check for correct definition of app_name. Generate CRUD views for
        all the models in the app.
        """
        if self.model_admins is None:
            self.model_admins = {}
        app_name = self.get_app_name()
        app = get_app(app_name)
        for model in get_models(app):
            model_name = model._meta.object_name
            if not model_name in self.model_admins:
                self.model_admins[model_name] = self.get_model_admin(model)

    def get_app_name(self):
        """
        Returns app_name or raise exception.
        """
        if self.app_name is None:
            raise ImproperlyConfigured(("BetterAppAdmin requires a definition "
                                        "of app_name in order to work."))
        return self.app_name

    def get_model_admin(self, model):
        """
        Returns a default BetterModelAdmin given a model.
        """
        klass = type('%sAdmin' % model._meta.object_name,
                    (BetterModelAdmin,),
                     dict(queryset=model.objects.all()))
        return klass()

    def get_nav(self):
        """
        Returns subclass of Nav that covers the ListViews for its models.
        """
        return type('%sNav' % self.app_name,
                    (Nav,),
                    dict(name=self.get_app_name().title(),
                         view=None,
                         options=[a.get_nav() for a in self.model_admins.values()]))

    def get_urls(self):
        """
        Gets url patterns from respective admins, merges and returns them.
        """
        urlpatterns = patterns('',)
        for model_admin in self.model_admins.values():
            urlpatterns += model_admin.get_urls()
        return urlpatterns
