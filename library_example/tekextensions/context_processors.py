from django.conf import settings
from django.contrib.sites.models import Site, RequestSite

def admin_media_prefix_deprecated(request):
    '''
    Alixedi: ADMIN_MEDIA_PREFIX has been deprecated starting from django 1.4
    '''
    return {'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX }

def admin_media_prefix(request):
    '''
    Starting from django 1.4, the static files belonging to django admin follow
    the standard conventions.
    '''
    return {'ADMIN_MEDIA_PREFIX': settings.STATIC_URL + 'admin/' }

def current_site(request):
    '''
    A context processor to add the "current_site" to the current Context
    '''
    context_name = 'CURRENT_SITE'

    try:
        current_site = Site.objects.get_current()
        return { context_name: current_site, }
    except Site.DoesNotExist:
        # always return a dict, no matter what!
        return { context_name: RequestSite(request)}
