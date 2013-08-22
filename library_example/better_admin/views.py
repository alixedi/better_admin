from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView
from better_admin.viewmixins import BetterListFilteredMixin, \
    SuccessMessageMixin
from better_admin.mixins import BetterMetaMixin
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django_actions.views import ActionViewMixin


class BetterListView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     BetterListFilteredMixin,
                     ActionViewMixin,
                     BetterMetaMixin,
                     ListView):
    '''
    A class-based generic list-view that requires the user to log-in, checks
    for specified permission, supports filtering using django-filters as well
    as pagination and sorting using django-tables2. All this on top of Django's
    already smashing class-based generic ListView which allows for custom
    templates, additional context data as well as user-specified context object
    names.

    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - BetterListFilteredMixin and BetterSingleTableMixin:
      better_admin/mixins.py
    - ListView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.list/\
      ListView/

    Usage example:
    # views.py
    class MyListView(BetterListView):
        model = MyModel
    # urls.py
    url(r'mymodel_list/', views.MyListView.as_view())
    '''
    pass


class BetterDetailView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       BetterMetaMixin,
                       DetailView):
    '''
    A class-based generic detail-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic DetailView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - DetailView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.detail/\
      DetailView/
    Usage example:
    # views.py
    class MyDetailView(BetterDetailView):
        model = MyModel
    # urls.py
    url(r'mymodel_detail/', views.MyDetailView.as_view())
    '''
    pass


class BetterCreateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       SuccessMessageMixin,
                       BetterMetaMixin,
                       CreateView):
    '''
    A class-based generic create-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic CreateView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - CreateView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.edit/\
      CreateView/
    Usage example:
    # views.py
    class MyCreateView(BetterCreateView):
        model = MyModel
    # urls.py
    url(r'mymodel_create/', views.MyCreateView.as_view())
    '''
    pass


class BetterUpdateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       SuccessMessageMixin,
                       BetterMetaMixin,
                       UpdateView):
    '''
    A class-based generic update-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic UpdateView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - UpdateView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.edit/\
      UpdateView/
    Usage example:
    # views.py
    class MyUpdateView(BetterUpdateView):
        model = MyModel
    # urls.py
    url(r'mymodel_update/', views.MyUpdateView.as_view())
    '''
    pass


class BetterDeleteView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       SuccessMessageMixin,
                       BetterMetaMixin,
                       DeleteView):
    '''
    A class-based generic delete-view that requires the user to log-in and
    checks for specified permission before proceeding. All this on top of
    Django's class-based generic DeleteView.
    Details about respective mixins can be found here:
    - LoginRequiredMixin and PermissionRequiredMixin:
      http://django-braces.readthedocs.org/en/latest/index.html
    - DeleteView:
      http://ccbv.co.uk/projects/Django/1.5/django.views.generic.edit/\
      DeleteView/
    Usage example:
    # views.py
    class MyDeleteView(BetterDeleteView):
        model = MyModel
    # urls.py
    url(r'mymodel_delete/', views.MyDeleteView.as_view())
    '''
    pass
