import hashlib

from django.contrib.auth.models import User
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from better_admin.core import BetterAppAdmin, BetterModelAdmin


class UserModelAdmin(BetterModelAdmin):
    model = User

    def pre_save(self, form, request):
        form.instance.password = hashlib.md5(form.instance.password).hexdigest()


class AuthAppAdmin(BetterAppAdmin):
    app_name = 'auth'
    model_admins = {'User': UserModelAdmin()}

    def get_urls(self):
        """
        Define extra urls.
        """

        urls = super(AuthAppAdmin, self).get_urls()

        urls += patterns('',

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
        )

        return urls


def enable_auth(urlpatterns, nav_groups):
    auth_app_admin = AuthAppAdmin()
    urlpatterns += auth_app_admin.get_urls()
    nav_groups.register(auth_app_admin.get_nav())