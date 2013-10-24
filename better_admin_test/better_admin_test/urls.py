from django.conf.urls import patterns
from django.conf.urls.static import static
from django.conf import settings

from django_nav import nav_groups

from better_admin.core import BetterAppAdmin
from better_admin.admin import enable_auth


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('') + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from better_admin_test_app.models import KAM
from better_admin.core import BetterModelAdmin
from better_admin_test_app.views import KAMBetterListView

class BetterKAMModelAdmin(BetterModelAdmin):
	queryset = KAM.objects.all()
	list_view = KAMBetterListView

	def get_request_queryset(self, request):
		return KAM.objects.filter(user=request.user)

class BetterAdminTestAppAdmin(BetterAppAdmin):
    app_name = 'better_admin_test_app'
    model_admins = {'KAM': BetterKAMModelAdmin()}

"""
class BetterAdminTestAppAdmin(BetterAppAdmin):
    app_name = 'better_admin_test_app'
"""

better_admin_test_app_admin = BetterAdminTestAppAdmin()
urlpatterns += better_admin_test_app_admin.get_urls()
nav_groups.register(better_admin_test_app_admin.get_nav())

enable_auth(urlpatterns, nav_groups)