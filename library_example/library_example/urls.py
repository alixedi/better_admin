from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('userena.urls')),
)


from better_admin.admin import BetterAppAdmin


class LibraryAdmin(BetterAppAdmin):
    app_name = 'library'

urlpatterns += LibraryAdmin().get_urls()
