from django.conf.urls import patterns
from django.conf.urls.static import static
from django.conf import settings

from django_nav import nav_groups

from better_admin.core import BetterAppAdmin
from better_admin.admin import AuthAppAdmin


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('') + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

class LibraryAppAdmin(BetterAppAdmin):
    app_name = 'library'

library_app_admin = LibraryAppAdmin()
urlpatterns += library_app_admin.get_urls()
nav_groups.register(library_app_admin.get_nav())


auth_app_admin = AuthAppAdmin()
urlpatterns += auth_app_admin.get_urls()
nav_groups.register(auth_app_admin.get_nav())