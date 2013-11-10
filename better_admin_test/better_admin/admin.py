import hashlib

from django.contrib.auth.models import User
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from better_admin.core import BetterAppAdmin, \
                              BetterModelAdmin
from better_admin.views import home
from better_admin.mixins import SUPERUSER_ACCESS


class UserModelAdmin(BetterModelAdmin):
    """
    Overriding UserModelAdmin in order to get around django's
    password md5 hack. 
    """
    queryset = User.objects.all()
    access = SUPERUSER_ACCESS
    list_exclude = ('password',)
    detail_exclude = ('password',)

    def create_pre_render(self, form, request):
        """
        Strip last login and date joined
        """
        del form.fields['last_login']
        del form.fields['date_joined']

    def update_pre_render(self, form, request):
        """
        Strip password and the like
        """
        del form.fields['password']
        del form.fields['last_login']
        del form.fields['date_joined']

    def create_pre_save(self, form, request):
        """
        Hash password
        """
        form.instance.password = hashlib.md5(form.instance.password).hexdigest()

class AuthAppAdmin(BetterAppAdmin):
    """
    AppAdmin for Auth. Obviously.
    """
    app_name = 'auth'
    model_admins = {'User': UserModelAdmin()}
    exclude = ['Permission',]

    def get_urls(self):
        """
        Define extra urls.
        """

        urls = super(AuthAppAdmin, self).get_urls()
        
        urls += patterns('',

            url(r'^$',
                home,
                name='home'),

            url(r'^auth/login/$',
                auth_views.login,
                {'template_name': 'auth/login.html'},
                name='auth_login'),

            url(r'^auth/logout/$',
                auth_views.logout,
                {'template_name': 'auth/logout.html'},
                name='auth_logout'),

            url(r'^auth/password/change/$',
                auth_views.password_change,
                {'template_name': 'auth/password_change_form.html'},
                name='auth_password_change'),

            url(r'^auth/password/change/done/$',
                auth_views.password_change_done,
                {'template_name': 'auth/password_change_done.html'},
                name='auth_password_change_done'),

            url(r'^auth/password/reset/$',
                auth_views.password_reset,
                {'template_name': 'auth/password_reset_form.html'},
                 name='auth_password_reset'),

            url(r'^auth/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                auth_views.password_reset_confirm,
                {'template_name': 'auth/password_reset_confirm.html'},
                name='auth_password_reset_confirm'),

            url(r'^auth/password/reset/complete/$',
                auth_views.password_reset_complete,
                {'template_name': 'auth/password_reset_complete.html'},
                name='auth_password_reset_complete'),

            url(r'^auth/password/reset/done/$',
                auth_views.password_reset_done,
                {'template_name': 'auth/password_change_done.html'},
                name='auth_password_reset_done'),
        )

        return urls


def enable_auth(urlpatterns, nav_groups):
    auth_app_admin = AuthAppAdmin()
    urlpatterns += auth_app_admin.get_urls()
    # Disabling this because we are customizing the auth nav in template!
    # nav_groups.register(auth_app_admin.get_nav())
