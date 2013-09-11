from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, url

from django_filters.filterset import filterset_factory

from better_admin.views import BetterListView, BetterDetailView, \
                               BetterCreateView, BetterUpdateView, \
                               BetterDeleteView, BetterPopupView


class BetterListAdminMixin(object):
    """
    Creates and takes care of ListView
    Requires the definition of get_queryset()
    """

    list_queryset = None
    list_view = None
    list_perm = None
    list_template = None
    filter_set = None
    actions = None

    def get_list_queryset(self):
        """
        Returns list queryset or default
        """
        if not self.list_queryset is None:
            return self.list_queryset
        else:
            return self.get_queryset()

    def get_list_perm(self):
        """
        Returns the given list perm or default
        """
        if not self.list_perm is None:
            return self.list_perm
        else:
            meta = self.get_list_queryset().model._meta
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
            model = self.get_list_queryset().model
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
            queryset = self.get_list_queryset()
            meta = queryset.model._meta
            name = '%sListView' % meta.object_name
            perm = self.get_list_perm()
            temp = self.get_list_template()
            filter_set = self.get_filter_set()
            actions = self.get_actions()

            return type(name,
                        (BetterListView,),
                        dict(queryset=queryset,
                             permission_required=perm,
                             template_name=temp,
                             filter_set=filter_set,
                             actions=actions))

    def get_list_urls(self):
        """
        Returns URLs for list view
        """
        meta = self.get_list_queryset().model._meta
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

    detail_queryset = None
    detail_view = None
    detail_perm = None
    detail_template = None

    def get_detail_queryset(self):
        """
        Returns detail queryset or default
        """
        if not self.detail_queryset is None:
            return self.detail_queryset
        else:
            return self.get_queryset()

    def get_detail_perm(self):
        """
        Returns the given perm or default
        """
        if not self.detail_perm is None:
            return self.detail_perm
        else:
            meta = self.get_detail_queryset().model._meta
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
            queryset = self.get_detail_queryset()
            meta = queryset.model._meta
            name = '%sDetailView' % meta.object_name
            perm = self.get_detail_perm()
            temp = self.get_detail_template()

            return type(name,
                        (BetterDetailView,),
                        dict(queryset=queryset,
                             permission_required=perm,
                             template_name=temp))

    def get_detail_urls(self):
        """
        Returns URLs for detail view
        """
        meta = self.get_detail_queryset().model._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_detail' % info
        detail_view = self.get_detail_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/(?P<pk>\d+)/$' % base_url,
                            detail_view.as_view(),
                            name=view_name))


class BetterCreateAdminMixin(object):
    """
    Creates and takes care of a CreateView
    Requires the definition of get_queryset()
    """
    create_queryset = None
    create_view = None
    create_perm = None
    create_form = None
    create_template = None
    create_success_url = None
    create_success_message = None

    def get_create_queryset(self):
        if not self.create_queryset is None:
            return self.create_queryset
        else:
            return self.get_queryset()

    def get_create_perm(self):
        """
        Returns the given perm or default
        """
        if not self.create_perm is None:
            return self.create_perm
        else:
            meta = self.get_create_queryset().model._meta
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
            meta = self.get_create_queryset().model._meta
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
            meta = self.get_create_queryset().model._meta
            return '%s was created successfully' % meta.object_name 

    def get_create_view(self):
        """
        Returns a create view 
        """
        if not self.create_view is None:
            return self.create_view
        else:
            queryset = self.get_create_queryset()
            meta = queryset.model._meta
            name = '%sCreateView' % meta.object_name
            perm = self.get_create_perm()
            temp = self.get_create_template()
            form = self.get_create_form()
            suc_url = self.get_create_success_url()
            suc_msg = self.get_create_success_message()

            return type(name,
                        (BetterCreateView,),
                        dict(queryset=queryset,
                             permission_required=perm,
                             template_name=temp,
                             form_class=form,
                             success_url=suc_url,
                             success_message=suc_msg))

    def get_create_urls(self):
        """
        Returns URLs for create view
        """
        meta = self.get_create_queryset().model._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_create' % info
        create_view = self.get_create_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/create/$' % base_url,
                            create_view.as_view(),
                            name=view_name))


class BetterPopupAdminMixin(object):

    popup_queryset = None
    popup_view = None
    popup_perm = None
    popup_form = None
    popup_template = None

    def get_popup_queryset(self):
        """
        Returns popup queryset or default
        """
        if not self.popup_queryset is None:
            return self.popup_queryset
        else:
            return self.get_queryset()

    def get_popup_perm(self):
        """
        Returns the given perm or default
        """
        if not self.popup_perm is None:
            return self.popup_perm
        else:
            meta = self.get_popup_queryset().model._meta
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

    def get_popup_view(self):
        """
        Returns a popup view 
        """
        if not self.popup_view is None:
            return self.popup_view
        else:
            queryset = self.get_popup_queryset()
            meta = queryset.model._meta
            name = '%sPopupView' % meta.object_name
            perm = self.get_popup_perm()
            temp = self.get_popup_template()
            form = self.get_popup_form()

            return type(name,
                        (BetterPopupView,),
                        dict(queryset=queryset,
                             permission_required=perm,
                             template_name=temp,
                             form_class=form))

    def get_popup_urls(self):
        """
        Returns URLs for popup view
        """
        meta = self.get_popup_queryset().model._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_popup' % info
        popup_view = self.get_popup_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/popup/$' % base_url,
                            popup_view.as_view(),
                            name=view_name))


class BetterUpdateAdminMixin(object):

    update_queryset = None
    update_view = None
    update_perm = None
    update_form = None
    update_view_template = None
    update_success_url = None
    update_success_message = None

    def get_update_queryset(self):
        """
        Returns update queryset or default
        """
        if not self.update_queryset is None:
            return self.update_queryset
        else:
            return self.get_queryset()

    def get_update_perm(self):
        """
        Returns the given perm or default
        """
        if not self.update_perm is None:
            return self.update_perm
        else:
            meta = self.get_update_queryset().model._meta
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
            meta = self.get_update_queryset().model._meta
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
            meta = self.get_update_queryset().model._meta
            return '%s was updated successfully' % meta.object_name 

    def get_update_view(self):
        """
        Returns a update view 
        """
        if not self.update_view is None:
            return self.update_view
        else:
            queryset = self.get_update_queryset()
            meta = queryset.model._meta
            name = '%sUpdateView' % meta.object_name
            perm = self.get_update_perm()
            temp = self.get_create_template()
            form = self.get_create_form()
            suc_url = self.get_update_success_url()
            suc_msg = self.get_create_success_message()

            return type(name,
                        (BetterUpdateView,),
                        dict(queryset=queryset,
                             permission_required=perm,
                             template_name=temp,
                             form_class=form,
                             success_url=suc_url,
                             success_message=suc_msg))

    def get_update_urls(self):
        """
        Returns URLs for update view
        """
        meta = self.get_popup_queryset().model._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_popup' % info
        update_view = self.get_update_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/(?P<pk>\d+)/update/$' % base_url,
                            update_view.as_view(),
                            name=view_name))


class BetterDeleteAdminMixin(object):

    delete_queryset = None
    delete_view = None
    delete_perm = None
    delete_form = None
    delete_template = None
    delete_success_url = None
    delete_success_message = None

    def get_delete_queryset(self):
        if not self.delete_queryset is None:
            return self.delete_queryset
        else:
            return self.get_queryset()

    def get_delete_perm(self):
        """
        Returns the given perm or default
        """
        if not self.delete_perm is None:
            return self.delete_perm
        else:
            meta = self.get_delete_queryset().model._meta
            info = meta.app_label.lower(), meta.object_name.lower()
            return '%s.remove_%s' % info

    def get_delete_template(self):
        """
        Returns the given template or default
        """
        if not self.delete_template is None:
            return self.delete_template
        else:
            return 'better_admin/create.html'

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
            meta = self.get_delete_queryset().model._meta
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
            meta = self.get_delete_queryset().model._meta
            return '%s was deleted successfully' % meta.object_name 

    def get_delete_view(self):
        """
        Returns a delete view 
        """
        if not self.delete_view is None:
            return self.delete_view
        else:
            queryset = self.get_delete_queryset()
            meta = queryset.model._meta
            name = '%sDeleteView' % meta.object_name
            perm = self.get_delete_perm()
            temp = self.get_delete_template()
            form = self.get_delete_form()
            suc_url = self.get_delete_success_url()
            suc_msg = self.get_delete_success_message()

            return type(name,
                        (BetterDeleteView,),
                        dict(queryset=queryset,
                             permission_required=perm,
                             template_name=temp,
                             form_class=form,
                             success_url=suc_url,
                             success_message=suc_msg))

    def get_delete_urls(self):
        """
        Returns URLs for delete view
        """
        meta = self.get_delete_queryset().model._meta
        info = meta.app_label.lower(), meta.object_name.lower()
        base_url = '%s/%s' % info
        view_name = '%s_%s_delete' % info
        delete_view = self.get_delete_view()

        return patterns('%s.views' % meta.app_label,
                        url(r'^%s/(?P<pk>\d+)/delete/$' % base_url,
                            delete_view.as_view(),
                            name=view_name))


class ReadOnlyModelAdminMixin(BetterListAdminMixin,
                              BetterDetailAdminMixin):
    """
    Read-only support. Does not support editing.
    """
    pass


class CreateOnlyModelAdminMixin(BetterListAdminMixin,
                                BetterDetailAdminMixin,
                                BetterCreateAdminMixin,
                                BetterPopupAdminMixin):
    """
    Create-onle support. Does not include editing or deleting.
    """
    pass


class CreateAndUpdateModelAdminMixin(BetterListAdminMixin,
                                     BetterDetailAdminMixin,
                                     BetterCreateAdminMixin,
                                     BetterPopupAdminMixin):
    """
    Create-onle support. Does not include editing or deleting.
    """
    pass


class BetterModelAdminMixin(BetterListAdminMixin,
                            BetterDetailAdminMixin,
                            BetterCreateAdminMixin,
                            BetterUpdateAdminMixin,
                            BetterDeleteAdminMixin,
                            BetterPopupAdminMixin):
    """
    Complete CRUD support.
    """
    pass