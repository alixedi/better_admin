from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import patterns, url

from better_admin.filters import TimeRangeFilter, \
                                 DateRangeFilter,\
                                 DateTimeRangeFilter, \
                                 filterset_factory

from better_admin.bulkmixins import BetterImportAdminMixin, \
                                    BetterExportAdminMixin

from better_admin.views import BetterListView, \
                               BetterStaffuserListView, \
                               BetterSuperuserListView

from better_admin.views import BetterDetailView, \
                               BetterStaffuserDetailView, \
                               BetterSuperuserDetailView
                               
from better_admin.views import BetterCreateView, \
                               BetterStaffuserCreateView, \
                               BetterSuperuserCreateView
                               
from better_admin.views import BetterUpdateView, \
                               BetterStaffuserUpdateView, \
                               BetterSuperuserUpdateView
                               
from better_admin.views import BetterDeleteView, \
                               BetterStaffuserDeleteView, \
                               BetterSuperuserDeleteView
                               
from better_admin.views import BetterPopupView, \
                               BetterStaffuserPopupView, \
                               BetterSuperuserPopupView

SUPERUSER_ACCESS = 0
STAFF_ACCESS = 1
GENERAL_ACCESS = 2


class BetterModelAdminMixin(object):
    """
    Generic functions that are required by Better<view_type>AdminMixins
    to work.
    """
    # this is mandatory!
    queryset = None
    # universal access
    access = None

    def get_model(self):
        """
        Returns self.queryset.model or raises an exception.
        """
        return self.get_queryset().model

    def get_model_name(self, lower=True):
        """
        Returns model name in a variety of formats
        """
        model_name = self.get_model()._meta.object_name
        return model_name.lower() if lower else model_name

    def get_app_label(self, lower=True):
        """
        Returns model name in a variety of formats
        """
        app_label = self.get_model()._meta.app_label
        return app_label.lower() if lower else app_label

    def get_queryset(self):
        """
        Returns self.queryset property. If None, raises an exception.
        """
        if not self.queryset is None:
            return self.queryset
        else:
            raise ImproperlyConfigured(("BetterModelAdmin requires a "
                                        "definition of queryset property."))

    def get_request_queryset(self, request):
        """
        This method is passed to the respective View where it is plugged into
        the get_queryset method. You can over-ride this to put in logic that
        generates the queryset dynamically based on request. For instance, 
        only showing contacts that are friends with request.user
        """
        return self.get_queryset()

    def get_perm(self, view_type):
        """
        This method returns the permission string in standard format given a 
        view_type. For instance, given 'list' as view_type, this method 
        returns '<app_name>.view_<model_name>' as the permission string.
        """
        # if user has overriden the perm for this specific view return that
        perm = getattr(self, '%s_perm' % view_type)
        if not perm is None:
            return perm
        # otherwise, create our own perm
        view_perm = {'list': 'view', 'detail': 'view',
                     'create': 'add', 'popup': 'add',
                     'update': 'change', 'delete': 'delete',
        }
        return '%s.%s_%s' % (self.get_app_label(), 
                             view_perm[view_type], 
                             self.get_model_name())

    def get_template(self, view_type):
        """
        This method returns the standard template path given a view_type.
        For instane, given 'list' as view_type, this method would return
        'better_admin/list.html'.
        """
        temp = getattr(self, '%s_template' % view_type)
        if not temp is None:
            return temp
        return 'better_admin/%s.html' % view_type

    def get_view_name(self, view_type):
        """
        This method returns the standard view_name for use in URL generation
        as well as in reverse and reverse_lazy etc given a view_type. For 
        instance, given 'list' as view_type, this method would return 
        '<app_label>_<model_name>_list'. 
        """
        return '%s_%s_%s' % (self.get_app_label(),
                             self.get_model_name(),
                             view_type)

    def get_base_url(self):
        return '%s/%s' % (self.get_app_label(), self.get_model_name())

    def get_form(self, view_type):
        """
        Returns the given form class or None
        """
        form = getattr(self, '%s_form' % view_type)
        if not form is None:
            return form
        else:
            # TODO: Intelligent Form Factory?
            return None

    def get_suc_url(self, view_type):
        """
        Returns the given success url or default
        """
        success_url = getattr(self, '%s_success_url' % view_type)
        if not success_url is None:
            return success_url
        else:
            view_name = self.get_view_name('list')
            return reverse_lazy(view_name)

    def get_suc_msg(self, view_type):
        """
        Returns the given success message or default
        """
        success_message = getattr(self, '%s_success_message' % view_type)
        if not success_message is None:
            return success_message
        else:
            return '%s was %sd successfully' % (self.get_model_name(),
                                                view_type)

    def pre_render(self, form, request):
        """
        Generic pre-render that is called by pre-renders of all views.
        This is here so that if we want to implement the same pre_render
        code across views, we only have to over-ride this.
        """
        pass

    def pre_save(self, form, request):
        """
        Generic pre-save that is called by pre-saves of all views.
        This is here so that if we want to implement the same pre_save
        code across views, we only have to over-ride this.
        """
        pass


class BetterListAdminMixin(object):
    """
    Creates and takes care of ListView
    """

    list_view = None
    list_access = GENERAL_ACCESS
    list_perm = None
    list_template = None
    filter_set = None
    actions = None

    def get_filter_set(self):
        """
        Returns given filter_set or default
        """
        if not self.filter_set is None:
            return self.filter_set
        else:
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

    def get_list_class(self):
        """
        Returns appropriate ListView class given access level.
        """
        access_class = {
            GENERAL_ACCESS: BetterListView,
            STAFF_ACCESS: BetterStaffuserListView,
            SUPERUSER_ACCESS: BetterSuperuserListView
        }
        if not self.access is None:
            return access_class[self.access]
        return access_class[self.list_access]

    def get_list_view(self):
        """
        Returns a list view 
        """
        if not self.list_view is None:
            return self.list_view
        else:
            return type('%sListView' % self.get_model_name(lower=False),
                        (self.get_list_class(),),
                        dict(model=self.get_model(),
                             queryset=self.get_queryset(),
                             request_queryset = self.get_request_queryset,
                             permission_required=self.get_perm('list'),
                             template_name=self.get_template('list'),
                             filter_set=self.get_filter_set(),
                             actions=self.get_actions()))

    def get_list_urls(self):
        """
        Returns URLs for list view
        """
        return patterns('%s.views' % self.get_app_label(),
                        url(r'^%s/$' % self.get_base_url(),
                            self.get_list_view().as_view(),
                            name=self.get_view_name('list')))


class BetterDetailAdminMixin(object):
    """
    Creates and takes care of a DetailView
    Requires the definition of get_queryset()
    """

    detail_view = None
    detail_perm = None
    detail_access = GENERAL_ACCESS
    detail_template = None

    def get_detail_class(self):
        """
        Returns appropriate DetailView class given access level.
        """
        access_class = {
            GENERAL_ACCESS: BetterDetailView,
            STAFF_ACCESS: BetterStaffuserDetailView,
            SUPERUSER_ACCESS: BetterSuperuserDetailView
        }
        if not self.access is None:
            return access_class[self.access]
        return access_class[self.detail_access]

    def get_detail_view(self):
        """
        Returns a detail view 
        """
        if not self.detail_view is None:
            return self.detail_view
        else:
            return type('%sDetailView' % self.get_model_name(lower=False),
                        (self.get_detail_class(),),
                        dict(model=self.get_model(),
                             queryset=self.get_queryset(),
                             request_queryset=self.get_request_queryset,
                             permission_required=self.get_perm('detail'),
                             template_name=self.get_template('detail')))

    def get_detail_urls(self):
        """
        Returns URLs for detail view
        """
        return patterns('%s.views' % self.get_app_label(),
                        url(r'^%s/(?P<pk>[a-zA-Z0-9_]+)/$' \
                                % self.get_base_url(),
                            self.get_detail_view().as_view(),
                            name=self.get_view_name('detail')))


class BetterCreateAdminMixin(object):
    """
    Creates and takes care of a CreateView
    Requires the definition of get_queryset()
    """
    create_view = None
    create_perm = None
    create_access = GENERAL_ACCESS
    create_form = None
    create_template = None
    create_success_url = None
    create_success_message = None

    def create_pre_render(self, form, request):
        """
        This function will be passed to the CreateView and will be executed
        just before the form is rendered. You may over-ride this and code
        useful logic such as removing and/or pre-setting fields.
        """
        self.pre_render(form, request)

    def create_pre_save(self, form, request):
        """
        This function will be passed to the CreateView and will be executed
        after validation and just before the form is saved. You may over-ride
        this and code useful logic such as removing and/or pre-setting fields.
        """
        self.pre_save(form, request)

    def get_create_class(self):
        """
        Returns appropriate CreateView class given access level.
        """
        access_class = {
            GENERAL_ACCESS: BetterCreateView,
            STAFF_ACCESS: BetterStaffuserCreateView,
            SUPERUSER_ACCESS: BetterSuperuserCreateView
        }
        if not self.access is None:
            return access_class[self.access]
        return access_class[self.create_access]

    def get_create_view(self):
        """
        Returns a create view 
        """
        if not self.create_view is None:
            return self.create_view
        else:
            return type('%sCreateView' % self.get_model_name(lower=False),
                        (self.get_create_class(),),
                        dict(queryset=self.get_queryset(),
                             request_queryset=self.get_request_queryset,
                             permission_required=self.get_perm('create'),
                             template_name=self.get_template('create'),
                             form_class=self.get_form('create'),
                             success_url=self.get_suc_url('create'),
                             success_message=self.get_suc_msg('create'),
                             pre_render=self.create_pre_render,
                             pre_save=self.create_pre_save))

    def get_create_urls(self):
        """
        Returns URLs for create view
        """
        return patterns('%s.views' % self.get_app_label(),
                        url(r'^%s/create/$' % self.get_base_url(),
                            self.get_create_view().as_view(),
                            name=self.get_view_name('create')))


class BetterPopupAdminMixin(object):
    """
    Creates and takes care of a PopupView
    Requires the definition of get_queryset()
    """
    popup_view = None
    popup_perm = None
    popup_access = GENERAL_ACCESS
    popup_form = None
    popup_template = None

    def popup_pre_render(self, form, request):
        """
        This function will be passed to the PopupView and will be executed
        just before the form is rendered. You may over-ride this and code
        useful logic such as removing and/or pre-setting fields.
        """
        self.pre_render(form, request)

    def popup_pre_save(self, form, request):
        """
        This function will be passed to the PopupView and will be executed
        after validation and just before the form is saved. You may over-ride
        this and code useful logic such as removing and/or pre-setting fields.
        """
        self.pre_save(form, request)

    def get_popup_class(self):
        """
        Returns appropriate PopupView class given access level.
        """
        access_class = {
            GENERAL_ACCESS: BetterPopupView,
            STAFF_ACCESS: BetterStaffuserPopupView,
            SUPERUSER_ACCESS: BetterSuperuserPopupView
        }
        if not self.access is None:
            return access_class[self.access]
        return access_class[self.popup_access]

    def get_popup_view(self):
        """
        Returns a popup view 
        """
        if not self.popup_view is None:
            return self.popup_view
        else:
            return type('%sPopupView' % self.get_model_name(lower=False),
                        (self.get_popup_class(),),
                        dict(queryset=self.get_queryset(),
                             request_queryset=self.get_request_queryset,
                             permission_required=self.get_perm('popup'),
                             template_name=self.get_template('popup'),
                             form_class=self.get_form('popup'),
                             pre_render=self.popup_pre_render,
                             pre_save=self.popup_pre_save))

    def get_popup_urls(self):
        """
        Returns URLs for popup view
        """
        return patterns('%s.views' % self.get_app_label(),
                        url(r'^%s/popup/$' % self.get_base_url(),
                            self.get_popup_view().as_view(),
                            name=self.get_view_name('popup')))


class BetterUpdateAdminMixin(object):
    """
    Creates and takes care of a UpdateView
    Requires the definition of get_queryset()
    """
    update_view = None
    update_perm = None
    update_access = GENERAL_ACCESS
    update_form = None
    update_template = None
    update_success_url = None
    update_success_message = None

    def update_pre_render(self, form, request):
        """
        This function will be passed to the UpdateView and will be executed
        just before the form is rendered. You may over-ride this and code
        useful logic such as removing and/or pre-setting fields.
        """
        self.pre_render(form, request)

    def update_pre_save(self, form, request):
        """
        This function will be passed to the UpdateView and will be executed
        after validation and just before the form is saved. You may over-ride
        this and code useful logic such as removing and/or pre-setting fields.
        """
        self.pre_save(form, request)

    def get_update_class(self):
        """
        Returns appropriate UpdateView class given access level.
        """
        access_class = {
            GENERAL_ACCESS: BetterUpdateView,
            STAFF_ACCESS: BetterStaffuserUpdateView,
            SUPERUSER_ACCESS: BetterSuperuserUpdateView
        }
        if not self.access is None:
            return access_class[self.access]
        return access_class[self.update_access]

    def get_update_view(self):
        """
        Returns a update view 
        """
        if not self.update_view is None:
            return self.update_view
        else:
            return type('%sUpdateView' % self.get_model_name(lower=False),
                        (self.get_update_class(),),
                        dict(queryset=self.get_queryset(),
                             request_queryset=self.get_request_queryset,
                             permission_required=self.get_perm('update'),
                             template_name=self.get_template('update'),
                             form_class=self.get_form('update'),
                             success_url=self.get_suc_url('update'),
                             success_message=self.get_suc_msg('update'),
                             pre_render=self.update_pre_render,
                             pre_save=self.update_pre_save))

    def get_update_urls(self):
        """
        Returns URLs for update view
        """
        return patterns('%s.views' % self.get_app_label(),
                        url(r'^%s/(?P<pk>[a-zA-Z0-9_]+)/update/$' \
                                % self.get_base_url(),
                            self.get_update_view().as_view(),
                            name=self.get_view_name('update')))


class BetterDeleteAdminMixin(object):
    """
    Creates and takes care of a DeleteView
    Requires the definition of get_queryset()
    """

    delete_view = None
    delete_perm = None
    delete_access = GENERAL_ACCESS
    delete_form = None
    delete_template = None
    delete_success_url = None
    delete_success_message = None

    def delete_pre_render(self, form, request):
        """
        This function will be passed to the DeleteView and will be executed
        just before the form is rendered. You may over-ride this and code
        useful logic such as removing and/or pre-setting fields.
        """
        self.pre_render(form, request)

    def delete_pre_save(self, form, request):
        """
        This function will be passed to the DeleteView and will be executed
        after validation and just before the form is saved. You may over-ride
        this and code useful logic such as removing and/or pre-setting fields.
        """
        self.pre_save(form, request)

    def get_delete_class(self):
        """
        Returns appropriate DeleteView class given access level.
        """
        access_class = {
            GENERAL_ACCESS: BetterDeleteView,
            STAFF_ACCESS: BetterStaffuserDeleteView,
            SUPERUSER_ACCESS: BetterSuperuserDeleteView
        }
        if not self.access is None:
            return access_class[self.access]
        return access_class[self.delete_access]

    def get_delete_view(self):
        """
        Returns a delete view 
        """
        if not self.delete_view is None:
            return self.delete_view
        else:
            return type('%sDeleteView' % self.get_model_name(lower=False),
                        (self.get_delete_class(),),
                        dict(queryset=self.get_queryset(),
                             request_queryset=self.get_request_queryset,
                             permission_required=self.get_perm('delete'),
                             template_name=self.get_template('delete'),
                             form_class=self.get_form('delete'),
                             success_url=self.get_suc_url('delete'),
                             success_message=self.get_suc_msg('delete'),
                             pre_render=self.delete_pre_render,
                             pre_save=self.delete_pre_save))

    def get_delete_urls(self):
        """
        Returns URLs for delete view
        """
        return patterns('%s.views' % self.get_app_label(),
                        url(r'^%s/(?P<pk>[a-zA-Z0-9_]+)/delete/$' \
                                % self.get_base_url(),
                            self.get_delete_view().as_view(),
                            name=self.get_view_name('delete')))


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
