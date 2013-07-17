from django.conf.urls import patterns, include, url
from django_nav import nav_groups

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('userena.urls')),
)


from better_admin.admin import BetterAppAdmin


class LibraryAdmin(BetterAppAdmin):
    app_name = 'library'

library_admin = LibraryAdmin()

urlpatterns += library_admin.get_urls()

nav_groups.register(library_admin.get_nav())
