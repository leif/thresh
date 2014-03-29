from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from thresh.main.views import RegistrationView,  ProposalCreateView, \
    ProposalList, PledgeCreateView,  CurrentPersonTransactionCreateView,  \
    CurrentPersonDetailView, CurrentPersonTransactionList

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # FIXME: change url to proposal/list?
    url(r'^$', ProposalList.as_view(), name='index'),
    # FIXME: change url to proposal/create?
    url(r'^create$',
        login_required(ProposalCreateView.as_view()),
        name='proposal_create'),

    url(r'(?P<proposal_id>\d+)/pledge/$',
        login_required(PledgeCreateView.as_view()),
        name='pledge_create'),

    url(r'^me/transaction/add$',
        login_required(CurrentPersonTransactionCreateView.as_view()),
        name='transaction_create'), 

    url(r'^me/$',
        login_required(CurrentPersonDetailView.as_view()),
        name='current_person_detail'), 

    # Examples:
    # url(r'^thresh/', include('thresh.foo.urls')),

    # django-registration
    # this url has to be before accounts/ to take precedence
    url(r'^accounts/register/$', RegistrationView.as_view(),
        #{ 'profile_callback': Person.objects.create },
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
