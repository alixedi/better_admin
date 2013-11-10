from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app, get_models
from django.conf.urls import patterns

from django_nav import Nav, NavOption
from django_nav.conditionals import user_has_perm

from better_admin.mixins import BetterModelAdminMixin


class BetterModelAdmin(BetterModelAdminMixin):
    """
    BetterModelAdmin creates and takes care of CRUD for the
    given model.
    """

    def get_nav(self):
        """
        Returns subclass of NavOption that points to the ListView of the model.
        """
        return type('%sNavOption' % self.get_model_name(),
                    (NavOption,),
                    dict(name=self.get_model_name().title(),
                         view=self.get_view_name('list'),
                         conditional = {'function': user_has_perm, 
                                        'args': [],
                                        'kwargs': {'perm': self.get_perm('list')}}))

    def get_urls(self):
        """
        Gets url patterns in order
        TODO: Use super call to get all urls compiled. Will have to rename
        get_<view_type>_urls to get_urls in all the mixins.
        """
        urls = patterns('%s.views' % self.get_app_label())
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
    exclude = None

    def __init__(self):
        """
        Check for correct definition of app_name. Generate CRUD views for
        all the models in the app.
        """
        if self.model_admins is None:
            self.model_admins = {}
        if self.exclude is None:
            self.exclude = []
        app_name = self.get_app_name()
        app = get_app(app_name)
        for model in get_models(app):
            model_name = model._meta.object_name
            if not model_name in self.model_admins:
                if model_name in self.exclude:
                    continue
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
