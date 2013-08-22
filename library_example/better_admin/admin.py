from better_admin.views import BetterListView, BetterDetailView, \
    BetterCreateView, BetterUpdateView, BetterDeleteView
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import patterns, url
from django.db.models import get_app, get_models
from django.core.urlresolvers import reverse_lazy
from django_nav import Nav, NavOption
from django_actions.actions import export_csv_action


class BetterModelAdmin(object):
    '''
    BetterModelAdmin tries to do what django's default ModelAdmin does. By
    saying 'tries', we are implicitly proposing slghtly tangent design goals
    as compared to the default ModelAdmin. Essentially, BetterModelAdmin
    provides a subset of the functionality present in the default ModelAdmin.
    However, it excels at being hackable right down to the nuts and bolts.
    For instance, at the moment, there are 2 levels hacking that is entirely
    supported by BetterModelAdmin:
    1. User can define custom templates.
    2. User can define custom CBVs.
    '''

    # This is necessary
    queryset = None

    # These are optional
    list_view = None
    create_view = None
    detail_view = None
    update_view = None
    delete_view = None

    # So are these
    list_view_template = None
    create_view_template = None
    detail_view_template = None
    update_view_template = None
    delete_view_template = None

    def __init__(self):
        '''
        Check for correct definition of queryset. Check for over-ride of any
        of the CRUD views, if not, generate sane defaults.
        '''
        # Have to define a queryset
        if self.queryset is None:
            raise ImproperlyConfigured(("BetterModelAdmin requires a "
                                        "definition of queryset property "
                                        "in order to work."))

        # If user hasn't specified his own views, provide good defaults
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

    def get_queryset(self):
        '''
        Returns self.queryset and if it is None, raises an ImproperlyConfigured
        exception. No need for this extra protection at the moment, but I am
        including this in view of any future modifications.
        '''
        if self.queryset is None:
            raise ImproperlyConfigured(("BetterModelAdmin requires a "
                                        "definition of queryset property "
                                        "in order to work."))
        return self.queryset

    def get_model(self):
        '''
        Returns the model of self.queryset
        '''
        queryset = self.get_queryset()
        return queryset.model

    def get_model_field_names(self):
        '''
        Returns the field names of model
        '''
        model = self.get_model()
        return model._meta.get_all_field_names()

    def get_model_name(self, lower=False, plural=False):
        '''
        Returns the model of that self.queryset belongs to, with support for
        lowercase as well as plural.
        '''
        ret = self.get_model()._meta.object_name
        if plural:
            ret = self.get_model()._meta.verbose_name_plural
        if lower:
            ret = ret.lower()
        return ret

    def get_app_name(self, lower=False):
        '''
        Reutrns the app name that the model for self.queryset belongs to, with
        support for lowercase.
        '''
        if lower:
            return self.get_model()._meta.app_label.lower()
        return self.get_model()._meta.app_label

    def get_template(self, viewtype):
        '''
        A universal getter for the <viewtype>_template property. Where viewtype
        can be list, detail, create, update or delete.
        '''
        user_template = getattr(self, '%s_view_template' % viewtype)
        if user_template is None:
            return 'better_admin/%s.html' % viewtype
        return user_template

    def get_permission(self, name, app=False):
        '''
        Formats permission strings given the name of the permission and whether
        one wants to include app name (<app_name>.<permission_name>_
        <model_name_lower>) or not (<permission_name>_<model_name_lower>)
        '''
        permission = '%s_%s' % (name, self.get_model_name(lower=True))
        if app:
            permission = '%s.%s' % (self.get_app_name(), permission)
        return permission

    def get_list_view(self):
        '''
        Factory method for BetterListView that returns a sane default.
        '''
        return type('ListView',
                    (BetterListView,),
                    dict(queryset=self.get_queryset(),
                         permission_required=self.get_permission('view', app=True),
                         template_name=self.get_template('list'),
                         actions=[export_csv_action, ]))

    def get_detail_view(self):
        '''
        Factory method for BetterDetailView that returns a sane default.
        '''
        return type('DetailView',
                    (BetterDetailView,),
                    dict(model=self.get_model(),
                         permission_required=self.get_permission('view', app=True),
                         template_name=self.get_template('detail')))

    def get_create_view(self):
        '''
        Factory method for BetterCreateView that returns a sane default.
        '''
        return type('CreateView',
                    (BetterCreateView,),
                    dict(model=self.get_model(),
                         permission_required=self.get_permission('add', app=True),
                         template_name=self.get_template('create'),
                         success_url=reverse_lazy(self.get_view_name('list')),
                         success_message="%s was created successfully" % self.get_model_name()))

    def get_update_view(self):
        '''
        Factory method for BetterUpdateView that returns a sane default.
        '''
        return type('UpdateView',
                    (BetterUpdateView,),
                    dict(model=self.get_model(),
                         permission_required=self.get_permission('modify', app=True),
                         template_name=self.get_template('update'),
                         # FIXME: Should redirect to DetailView on success!
                         success_url=reverse_lazy(self.get_view_name('list')),
                         success_message="%s was updated successfully" % self.get_model_name()))

    def get_delete_view(self):
        '''
        Factory method for BetterDeleteView that returns a sane default.
        '''
        return type('DeleteView',
                    (BetterDeleteView,),
                    dict(model=self.get_model(),
                         permission_required=self.get_permission('delete', app=True),
                         template_name=self.get_template('delete'),
                         success_url=reverse_lazy(self.get_view_name('list')),
                         success_message="%s was deleted successfully" % self.get_model_name()))

    def get_base_url(self):
        '''
        Returns the base url for wherever the model of the specified queryset
        happens to lie. The base url will be <app_name_lower>/
        <model_name_lower_plural>
        '''
        return '%s/%s' % (self.get_app_name(lower=True),
                          self.get_model_name(lower=True, plural=True))

    def get_view_name(self, viewtype):
        '''
        Returns a friendly name for our view for use in reverse and the likes.
        Convention goes like this: <app_name_lower>_<model_name_lower>_
        <viewtype> where viewtype are the usual CRUD suspects.
        '''
        return '%s_%s_%s' % (self.get_app_name(lower=True),
                             self.get_model_name(lower=True),
                             viewtype)

    def get_nav(self):
        '''
        Returns subclass of NavOption that points to the ListView of the model.
        '''
        return type('%sNavOption' % self.get_model_name(),
                    (NavOption,),
                    dict(name=self.get_model_name(plural=True),
                         view=self.get_view_name('list')))

    def get_urls(self):
        '''
        Masterpiece plugs into the urls.py and generate default patterns in
        order to keep things DRY. Following are the conventions in force:
        list_view: /app_name/model_name_plural/
        create_view: /app_name/model_name_plural/create
        detail_view: /app_name/model_name_plural/pk
        update_view: /app_name/model_name_plural/pk/update
        delete_view: /app_name/model_name_plural/pk/delete
        '''

        return patterns(

            '%s.views' % self.get_app_name(),

            url(r'^%s/create$' % self.get_base_url(),
                self.create_view.as_view(),
                name=self.get_view_name('create')),

            url(r'^%s/(?P<pk>\d+)$' % self.get_base_url(),
                self.detail_view.as_view(),
                name=self.get_view_name('detail')),

            url(r'^%s/(?P<pk>\d+)/update$' % self.get_base_url(),
                self.update_view.as_view(),
                name=self.get_view_name('update')),

            url(r'^%s/(?P<pk>\d+)/delete$' % self.get_base_url(),
                self.delete_view.as_view(),
                name=self.get_view_name('delete')),

            url(r'^%s/' % self.get_base_url(),
                self.list_view.as_view(),
                name=self.get_view_name('list')),
        )


class BetterAppAdmin(object):
    '''
    Given a django app, this basically introspects the app, extracts all the
    models and then goes on to create BetterModelAdmins with reasonable
    defaults for each of the model. Moreover, if you want to do something
    special for the BetterModelAdmin of one of the models, this allows you
    to bring your own class and override the defaults. Notice that if you
    want, you may override with a None in order to not have any admin for
    the model of your choice.
    '''

    # This is necessary
    app_name = None

    # This is where we dump all the objects
    model_admins = {}

    def __init__(self):
        '''
        Check for correct definition of app_name. Generate CRUD views for
        all the models in the app.
        '''
        # Have to define an app
        if self.app_name is None:
            raise ImproperlyConfigured(("BetterAppAdmin requires a definition "
                                        "of app_name in order to work."))
        # For each model in the app
        app = get_app(self.app_name)
        for model in get_models(app):
            model_name = model._meta.object_name
            if not model_name in self.model_admins:
                self.model_admins[model_name] = self.get_model_admin(model)

    def get_app_name(self):
        if self.app_name is None:
            raise ImproperlyConfigured(("BetterAppAdmin requires a definition "
                                        "of app_name in order to work."))
        return self.app_name

    def get_model_admin(self, model):
        '''
        Returns a default BetterModelAdmin given a model.
        '''
        klass = type('%sAdmin' % model._meta.object_name,
                    (BetterModelAdmin,),
                     dict(queryset=model.objects.all()))
        return klass()

    def get_nav(self):
        '''
        Returns subclass of Nav that covers the ListViews for its models.
        '''
        return type('%sNav' % self.app_name,
                    (Nav,),
                    dict(name=self.get_app_name().title(),
                         view=None,
                         options=[a.get_nav() for a in self.model_admins.values()]))

    def get_urls(self):
        '''
        Gets url patterns from respective admins, merges and returns them.
        '''
        urlpatterns = patterns('',)
        for model_admin in self.model_admins.values():
            urlpatterns += model_admin.get_urls()
        return urlpatterns
