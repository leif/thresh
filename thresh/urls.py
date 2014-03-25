from django.conf.urls import patterns, include, url

from thresh.main.views import RegistrationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'thresh.main.views.index', name='index'),
    url(r'^create$', 'thresh.main.views.create', name='create'),

    # Examples:
    # url(r'^thresh/', include('thresh.foo.urls')),

    # django-registration
    # this url has to be before accounts/ to take precedence
    url(r'^accounts/register/$', RegistrationView.as_view(),
        name='registration_register'),
    # FIXME: for development only, use one-step backend,
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # change to two steps for production
    #url(r'^accounts/', include('registration.backends.default.urls')),

    # for django auth, i.e. x/password/change/ (not included in
    # django-registration)
    url(r'^accounts/', include('django.contrib.auth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
