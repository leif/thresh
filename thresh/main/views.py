from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from registration.backends.simple.views import RegistrationView \
    as _RegistrationView

from thresh.main.models import Proposal,  Person

#FIXME: logging settings
import logging
logger = logging.getLogger(__name__)


class ProposalList(ListView):
    #template_name = 'user_list.html'
    model = Proposal
    queryset = Proposal.objects.all().order_by('-created')

class ProposalCreateView(CreateView):

    model = Proposal
    # FIXME: use named urls
    success_url = '/'

    # set field creater to the current logged in user
    def form_valid(self, form):
        logger.debug('in ProposalCreateView form_valid')
        print 'in in ProposalCreateView form_valid'
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        return super(ProposalCreateView, self).form_valid(form) 

class RegistrationView(_RegistrationView):
    def get_success_url(self,  request,  user):
        """
        Override the default redirect url to index page instead of the default
        one, /users/<username>/
        """
        return ('index', (), {})
