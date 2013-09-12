from django.views.generic import ListView, DetailView, CreateView, \
                                 UpdateView, DeleteView

from better_admin.viewmixins import ListFilteredMixin, SuccessMessageMixin, \
                                    HookMixin, PopupMixin, BaseViewMixin, \
                                    TemplateUtilsMixin

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from django_actions.views import ActionViewMixin


class BetterListView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     ListFilteredMixin,
                     ActionViewMixin,
                     TemplateUtilsMixin,
                     BaseViewMixin,
                     ListView):
    """
    A class-based generic list-view that requires the user to log-in, checks
    for specified permission, supports filtering using django-filters as well
    as pagination and sorting using django-pagination and django-sorting. All 
    this on top of Django's already smashing class-based generic ListView.

    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - ListFilteredMixin and MetaMixin:
      better_admin/viewmixins.py
    - ListView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.list/\
      ListView/

    Usage example:
    # views.py
    class MyListView(BetterListView):
        model = MyModel
    # urls.py
    url(r'mymodel_list/', views.MyListView.as_view())
    """
    pass


class BetterDetailView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       TemplateUtilsMixin,
                       BaseViewMixin,
                       DetailView):
    """
    A class-based generic detail-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic DetailView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - MetaMixin:
      better_admin/viewmixins.py
    - DetailView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.detail/\
      DetailView/

    Usage example:
    # views.py
    class MyDetailView(BetterDetailView):
        model = MyModel
    # urls.py
    url(r'mymodel_detail/', views.MyDetailView.as_view())
    """
    pass


class BetterCreateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       SuccessMessageMixin,
                       HookMixin,
                       TemplateUtilsMixin,
                       BaseViewMixin,
                       CreateView):
    """
    A class-based generic create-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic CreateView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - HookMixin and MetaMixin:
      better_admin/viewmixins.py
    - CreateView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.edit/\
      CreateView/

    Usage example:
    # views.py
    class MyCreateView(BetterCreateView):
        model = MyModel
    # urls.py
    url(r'mymodel_create/', views.MyCreateView.as_view())
    """
    pass


class BetterPopupView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      SuccessMessageMixin,
                      PopupMixin,
                      TemplateUtilsMixin,
                      BaseViewMixin,
                      CreateView):
    """
    A class-based generic create-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic CreateView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - PopupMixin and MetaMixin:
      better_admin/viewmixins.py
    - CreateView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.edit/\
      CreateView/

    Usage example:
    # views.py
    class MyPopupView(BetterPopupView):
        model = MyModel
    # urls.py
    url(r'mymodel_create/', views.MyCreateView.as_view())
    """
    pass

class BetterUpdateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       SuccessMessageMixin,
                       HookMixin,
                       TemplateUtilsMixin,
                       BaseViewMixin,
                       UpdateView):
    """
    A class-based generic update-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic UpdateView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - HookMixin and MetaMixin:
      better_admin/viewmixins.py
    - UpdateView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.edit/\
      UpdateView/

    Usage example:
    # views.py
    class MyUpdateView(BetterUpdateView):
        model = MyModel
    # urls.py
    url(r'mymodel_update/', views.MyUpdateView.as_view())
    """
    pass


class BetterDeleteView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       SuccessMessageMixin,
                       HookMixin,
                       TemplateUtilsMixin,
                       BaseViewMixin,
                       DeleteView):
    """
    A class-based generic delete-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic DeleteView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - MetaMixin:
      better_admin/viewmixins.py
    - DeleteView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.edit/\
      DeleteView/

    Usage example:
    # views.py
    class MyDeleteView(BetterDeleteView):
        model = MyModel
    # urls.py
    url(r'mymodel_delete/', views.MyDeleteView.as_view())
    """
    pass
