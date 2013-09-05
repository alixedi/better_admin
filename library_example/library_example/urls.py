from django.conf.urls import patterns, include, url
from django_nav import nav_groups
from django.conf.urls.static import static
from django.conf import settings
from library.models import Tariff, Company, KAM

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('userena.urls')),
    url(r'^add/(?P<model_name>\w+)/?$', 
        'tekextensions.views.add_new_model', 
        name='add_new'),
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

from better_admin.admin import BetterAppAdmin, BetterModelAdmin

class TariffModelAdmin(BetterModelAdmin):
    #queryset = Tariff.objects.all()
    queryset = Tariff.objects.filter(company__name='Bhaoo')
    #filter_set = TariffFilterSet

    def pre_render(self, form, request):
        #del form.fields['company']
        form.fields['kams'].queryset = KAM.objects.filter(permanent=True)

    #def pre_save(self, form, request):
        #form.instance.company = Company.objects.get(name='Bhaoo')

class LibraryAdmin(BetterAppAdmin):
    app_name = 'library'
    model_admins = {'Tariff': TariffModelAdmin()}


library_admin = LibraryAdmin()
urlpatterns += library_admin.get_urls()
nav_groups.register(library_admin.get_nav())
