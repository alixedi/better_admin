from django.core.exceptions import ImproperlyConfigured

from better_admin.crudmixins import BetterListAdminMixin, \
                                    BetterDetailAdminMixin, \
                                    BetterCreateAdminMixin, \
                                    BetterPopupAdminMixin, \
                                    BetterUpdateAdminMixin, \
                                    BetterDeleteAdminMixin

from better_admin.importexportmixins import BetterExportAdminMixin, \
                                            BetterImportAdminMixin


class BetterModelAdminBaseMixin(object):
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
                              BetterModelAdminBaseMixin):
    """
    Read-only support. Does not support editing.
    """
    pass


class CreateOnlyModelAdminMixin(BetterListAdminMixin,
                                BetterDetailAdminMixin,
                                BetterCreateAdminMixin,
                                BetterPopupAdminMixin,
                                BetterModelAdminBaseMixin):
    """
    Create-onle support. Does not include editing or deleting.
    """
    pass


class CreateAndUpdateModelAdminMixin(BetterListAdminMixin,
                                     BetterDetailAdminMixin,
                                     BetterCreateAdminMixin,
                                     BetterPopupAdminMixin,
                                     BetterModelAdminBaseMixin):
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
                            BetterModelAdminBaseMixin):
    """
    Complete CRUD support.
    """
    pass