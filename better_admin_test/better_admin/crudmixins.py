from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, url

from django_filters.filterset import filterset_factory

from better_admin.views import BetterListView, \
                               BetterSuperuserListView, \
                               BetterStaffuserListView

from better_admin.views import BetterDetailView, \
                               BetterSuperuserDetailView, \
                               BetterStaffuserDetailView

from better_admin.views import BetterCreateView, \
                               BetterSuperuserCreateView, \
                               BetterStaffuserCreateView

from better_admin.views import BetterUpdateView, \
                               BetterSuperuserUpdateView, \
                               BetterStaffuserUpdateView

from better_admin.views import BetterDeleteView, \
                               BetterSuperuserDeleteView, \
                               BetterStaffuserDeleteView

from better_admin.views import BetterPopupView, \
                               BetterSuperuserPopupView, \
                               BetterStaffuserPopupView                                


class BetterListAdminMixin(object):
    """
    Creates and takes care of ListView
    """

    list_view = None
    list_template = None
    filter_set = None
    actions = None
    # permission related properties
    list_perm = None
    list_superuser_reqd = None
    list_staffuser_reqd = None

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

    def get_listview_klass(self):
        """
        Returns the ListView class to be used
        """
        superuser = self.list_superuser_reqd
        staffuser = self.list_staffuser_reqd
        if not superuser is None and superuser is True:
            return BetterSuperuserListView
        if not staffuser is None and staffuser is True:
            return BetterStaffuserListView
        else:
            return BetterListView

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
            klass = self.get_listview_klass()

            return type(name,
                        (klass,),
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
    detail_template = None
    # permission related properties
    detail_perm = None
    detail_superuser_reqd = None
    detail_staffuser_reqd = None

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

    def get_detailview_klass(self):
        """
        Returns the DetailView class to be used
        """
        superuser = self.detail_superuser_reqd
        staffuser = self.detail_staffuser_reqd
        if not superuser is None and superuser is True:
            return BetterSuperuserDetailView
        if not staffuser is None and staffuser is True:
            return BetterStaffuserDetailView
        else:
            return BetterDetailView

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
            klass = self.get_detailview_klass()

            return type(name,
                        (klass,),
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
    create_form = None
    create_template = None
    create_success_url = None
    create_success_message = None
    # permission related properties
    create_perm = None
    create_superuser_reqd = None
    create_staffuser_reqd = None

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

    def get_createview_klass(self):
        """
        Returns the CreateView class to be used
        """
        superuser = self.create_superuser_reqd
        staffuser = self.create_staffuser_reqd
        if not superuser is None and superuser is True:
            return BetterSuperuserCreateView
        if not staffuser is None and staffuser is True:
            return BetterStaffuserCreateView
        else:
            return BetterCreateView

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
            klass = self.get_createview_klass()

            return type(name,
                        (klass,),
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
    popup_form = None
    popup_template = None
    # permission related properties
    popup_perm = None
    popup_superuser_reqd = None
    popup_staffuser_reqd = None

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

    def get_popupview_klass(self):
        """
        Returns the PopupView class to be used
        """
        superuser = self.popup_superuser_reqd
        staffuser = self.popup_staffuser_reqd
        if not superuser is None and superuser is True:
            return BetterSuperuserPopupView
        if not staffuser is None and staffuser is True:
            return BetterStaffuserPopupView
        else:
            return BetterPopupView

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
            klass = self.get_popupview_klass()

            return type(name,
                        (klass,),
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
    update_form = None
    update_template = None
    update_success_url = None
    update_success_message = None
    # permission related properties
    update_perm = None
    update_superuser_reqd = None
    update_staffuser_reqd = None

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

    def get_updateview_klass(self):
        """
        Returns the UpdateView class to be used
        """
        superuser = self.update_superuser_reqd
        staffuser = self.update_staffuser_reqd
        if not superuser is None and superuser is True:
            return BetterSuperuserUpdateView
        if not staffuser is None and staffuser is True:
            return BetterStaffuserUpdateView
        else:
            return BetterUpdateView

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
            klass = self.get_updateview_klass()

            return type(name,
                        (klass,),
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
    delete_form = None
    delete_template = None
    delete_success_url = None
    delete_success_message = None
    # permission related properties
    delete_perm = None
    delete_superuser_reqd = None
    delete_staffuser_reqd = None

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

    def get_deleteview_klass(self):
        """
        Returns the DeleteView class to be used
        """
        superuser = self.delete_superuser_reqd
        staffuser = self.delete_staffuser_reqd
        if not superuser is None and superuser is True:
            return BetterSuperuserDeleteView
        if not staffuser is None and staffuser is True:
            return BetterStaffuserDeleteView
        else:
            return BetterDeleteView

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
            klass = self.get_deleteview_klass()

            return type(name,
                        (klass,),
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
