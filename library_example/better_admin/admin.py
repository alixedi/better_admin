from better_admin.views import BetterListView, BetterDetailView, \
    BetterCreateView, BetterUpdateView, BetterDeleteView
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import patterns, url
from django.db.models import get_app, get_models


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

    def __init__(self):
        '''
        Check for correct definition of queryset. Check for over-ride of any
        of the CRUD views, if not, generate sane defaults.
        '''
        # Have to define a querysey
        if self.queryset is None:
            raise ImproperlyConfigured(
                '''BetterModelAdmin requires a definition of \
                queryset property in order to work.''')

        # If user hasn't specified his own views, provide good defaults
        self.list_view = getattr(self, 'list_view', self.get_list_view())
        self.detail_view = getattr(self, 'detail_view', self.get_detail_view())
        self.create_view = getattr(self, 'create_view', self.get_create_view())
        self.update_view = getattr(self, 'update_view', self.get_update_view())
        self.delete_view = getattr(self, 'delete_view', self.get_delete_view())

    def get_model_name(self, lower=False, plural=False):
        '''
        Returns the model of that self.queryset belongs to, with support for
        lowercase as well as plural.
        '''
        ret = self.queryset.model._meta.object_name
        if plural:
            ret = self.queryset.model._meta.verbose_name_plural
        if lower:
            return ret.lower()
        return ret

    def get_app_name(self, lower=False):
        '''
        Reutrns the app name that the model for self.queryset belongs to, with
        support for lowercase.
        '''
        if lower:
            return self.queryset.model._meta.app_label.lower()
        return self.queryset.model._meta.app_label

    def get_template(self, viewtype):
        '''
        A universal getter for the <viewtype>_template property. Where viewtype
        can be list, detail, create, update or delete.
        '''
        return getattr(self,
                       '%s_view_template' % viewtype,
                       'better_admin/%s.html' % viewtype)

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
        class ListView(BetterListView):
            queryset = self.queryset
            permission_required = self.get_permission('view', app=True)
            template_name = self.get_template('list')
        return ListView

    def get_detail_view(self):
        '''
        Factory method for BetterDetailView that returns a sane default.
        '''
        class DetailView(BetterDetailView):
            model = self.queryset.model
            permission_required = self.get_permission('view', app=True)
            template_name = self.get_template('detail')
        return DetailView

    def get_create_view(self):
        '''
        Factory method for BetterCreateView that returns a sane default.
        '''
        class CreateView(BetterCreateView):
            model = self.queryset.model
            permission_required = self.get_permission('add', app=True)
            template_name = self.get_template('create')
        return CreateView

    def get_update_view(self):
        '''
        Factory method for BetterUpdateView that returns a sane default.
        '''
        class UpdateView(BetterUpdateView):
            model = self.queryset.model
            permission_required = self.get_permission('modify', app=True)
            template_name = self.get_template('update')
        return UpdateView

    def get_delete_view(self):
        '''
        Factory method for BetterDeleteView that returns a sane default.
        '''
        class DeleteView(BetterDeleteView):
            model = self.queryset.model
            permission_required = self.get_permission('delete', app=True)
            template_name = self.get_template('delete')
        return DeleteView

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
    Warning, this is now getting to ridiculous proportions. I do not think
    anyone would ever need to go here. However, as for first-cuts go, this
    will provide a reasonable one.
    '''

    # This is necessary
    app_name = None

    # This is where we dump all the objects
    admins = {}

    def __init__(self):
        '''
        Check for correct definition of app_name. Generate CRUD views for
        all the models in the app.
        '''
        # Have to define an app
        if self.app_name is None:
            raise ImproperlyConfigured(
                '''BetterAppAdmin requires a definition of \
                app_name property in order to work.''')
        # For each model in the app
        app = get_app(self.app_name)
        for model in get_models(app):
            self.admins[model._meta.object_name] = self.get_model_admin(model)

    def get_model_admin(self, model):
        '''
        Returns a default BetterModelAdmin given a model.
        '''
        klass = type('%sAdmin' % model._meta.object_name,
                    (BetterModelAdmin,),
                     dict(queryset=model.objects.all()))
        return klass()

    def get_urls(self):
        '''
        Gets url patterns from respective admins, merges and returns them.
        '''
        urlpatterns = patterns('',)
        for admin in self.admins.values():
            print admin.get_urls()
            urlpatterns += admin.get_urls()
        print urlpatterns
        return urlpatterns
