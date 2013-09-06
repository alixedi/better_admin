from django.conf.urls import patterns, include, url
from django_nav import nav_groups
from django.conf.urls.static import static
from django.conf import settings
from library.models import Tariff, Company, KAM
from django.contrib.auth import views as auth_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^accounts/login/$',
       auth_views.login,
       {'template_name': 'accounts/login.html'},
       name='auth_login'),

    url(r'^accounts/logout/$',
       auth_views.logout,
       {'template_name': 'accounts/logout.html'},
       name='auth_logout'),

    url(r'^accounts/password/change/$',
       auth_views.password_change,
       {'template_name': 'accounts/password_change_form.html'},
       name='auth_password_change'),

    url(r'^accounts/password/change/done/$',
       auth_views.password_change_done,
       {'template_name': 'accounts/password_change_done.html'},
       name='auth_password_change_done'),

    url(r'^accounts/password/reset/$',
       auth_views.password_reset,
       {'template_name': 'accounts/password_reset_form.html'},
       name='auth_password_reset'),

    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'accounts/password_reset_confirm.html'},
       name='auth_password_reset_confirm'),

    url(r'^accounts/password/reset/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'accounts/password_reset_complete.html'},
       name='auth_password_reset_complete'),

    url(r'^accounts/password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'accounts/password_change_done.html'},
       name='auth_password_reset_done'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


import django_filters

class TariffFilterSet(django_filters.FilterSet):
    class Meta:
        model = Tariff
        fields = ['codes', 'expired']
    def __init__(self, *args, **kwargs):
        super(TariffFilterSet, self).__init__(*args, **kwargs)
        self.filters['codes'].lookup_type = None
        print type(self.filters['codes'])

from django.forms import ModelForm

class TariffForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TariffForm, self).__init__(*args, **kwargs)
        self.fields['kams'].queryset = KAM.objects.filter(permanent=True)

    def save(self):
        instance = super(TariffForm, self).save(commit=False)
        instance.save()
        return instance

    class Meta:
        model = Tariff
        exclude = ['company']


from better_admin.admin import BetterAppAdmin, BetterModelAdmin

class TariffModelAdmin(BetterModelAdmin):
    queryset = Tariff.objects.all()
    #filter_set = TariffFilterSet
    #create_form = TariffForm
    #update_form = TariffForm

    def pre_render(self, form, request):
        for key in request.GET:
            try:
                form.fields[key].initial = request.GET[key]
                form.fields[key].widget.attrs['disabled'] = 'disabled'
            except KeyError:
                pass

    #def pre_save(self, form, request):
        #form.instance.company = Company.objects.get(name='Bhaoo')

class KAMAdmin(BetterModelAdmin):
    queryset = KAM.objects.all()

    def pre_render(self, form, request):
        del form.fields['user']

    def pre_save(self, form, request):
        form.instance.user = request.user

class LibraryAdmin(BetterAppAdmin):
    app_name = 'library'
    model_admins = {'Tariff': TariffModelAdmin(),
                    'KAM': KAMAdmin()}

library_admin = LibraryAdmin()
urlpatterns += library_admin.get_urls()
nav_groups.register(library_admin.get_nav())












from django.contrib.auth.models import User
import hashlib

class UserModelAdmin(BetterModelAdmin):
    queryset = User.objects.all()

    def pre_save(self, form, request):
        form.instance.password = hashlib.md5(form.instance.password).hexdigest()


class AuthAdmin(BetterAppAdmin):
    app_name = 'auth'
    model_admins = {'User': UserModelAdmin()}

auth_admin = AuthAdmin()
urlpatterns += auth_admin.get_urls()
nav_groups.register(auth_admin.get_nav())

