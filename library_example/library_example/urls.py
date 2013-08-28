from django.conf.urls import patterns, include, url
from django_nav import nav_groups
from django.conf.urls.static import static
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('userena.urls')),
    url(r'^add/(?P<model_name>\w+)/?$', 
    	'tekextensions.views.add_new_model', 
    	name='add_new'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from better_admin.admin import BetterAppAdmin


class LibraryAdmin(BetterAppAdmin):
    app_name = 'library'

library_admin = LibraryAdmin()
urlpatterns += library_admin.get_urls()
nav_groups.register(library_admin.get_nav())
