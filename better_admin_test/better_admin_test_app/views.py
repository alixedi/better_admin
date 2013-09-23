from django_filters.filterset import filterset_factory

from better_admin.views import BetterListView

from better_admin_test_app.models import KAM


class KAMBetterListView(BetterListView):
	model = KAM
	permission_required = 'better_admin_test_app.view_kam'
	template_name = 'better_admin/list.html'
	filter_set = filterset_factory(KAM)

	def get_request_queryset(self, request):
		return self.model.queryset.all()