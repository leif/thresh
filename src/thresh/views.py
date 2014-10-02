from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView,  UpdateView
from django.views.generic import ListView,  DetailView

from registration.backends.simple.views import RegistrationView \
    as _RegistrationView

from thresh.models import Proposal, Person, Pledge, Transaction
from thresh.forms import PledgeForm,  CurrentPersonTransactionForm

import logging
logger = logging.getLogger('thresh')


class ProposalList(ListView):
    #template_name = 'user_list.html'
    model = Proposal
    queryset = Proposal.objects.all().order_by('-created')


class ProposalDetailView(DetailView):
    model = Proposal


class ProposalCreateView(CreateView):

    model = Proposal


    def get_success_url(self):
        return reverse('index')


    # set field creater to the current logged in user
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        logger.debug("Creating proposal")
        return super(ProposalCreateView, self).form_valid(form)


class PledgeCreateView(CreateView):
    model = Pledge
    form_class = PledgeForm


    def get_success_url(self):
        return reverse('index')


    def get_initial(self, *args, **kwargs):
        proposal = get_object_or_404(Proposal, pk=self.kwargs['proposal_id'])

        # person object is passed as a hidden input to the form instead of
        # to instantiate it in the
        # form_valid method cause it is needed before,
        # in the form clean method,
        person = self.request.user
        return {'proposal': proposal,  'person': person}


    def dispatch(self, request, *args, **kwargs):
        """
        Redirect to pledge update view if the pledge for this proposal and
        logged in person exists.
        """
        person = self.request.user
        proposal = get_object_or_404(Proposal, pk=self.kwargs['proposal_id'])
        pledge = person.get_pledge_on_proposal(proposal)
        if pledge:
            logger.debug('pledge already exists, redirecting to update plege')
            return redirect('pledge_update',
                            proposal_id=proposal.id,
                            pk=pledge.id)
        logger.debug('creating pledge')
        return super(PledgeCreateView, self).dispatch(request, *args, **kwargs)


    def get_percent_backed(self):
        return sum( pledge.amount for pledge in self.pledge_set.all() if pledge.is_backed() ) / float( self.threshold )


class PledgeUpdateView(UpdateView):
    model = Pledge
    form_class = PledgeForm
    template_name = 'thresh/pledge_update_form.html'


    def get_success_url(self):
        return reverse('index')


    def get_initial(self, *args, **kwargs):
        proposal = get_object_or_404(Proposal, pk=self.kwargs['proposal_id'])
        person = self.request.user
        return {'proposal': proposal,  'person': person}


class CurrentPersonTransactionCreateView(CreateView):

    model = Transaction
    form_class = CurrentPersonTransactionForm

    # set field creater to the current logged in user
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.person = self.request.user
        return super(CurrentPersonTransactionCreateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('current_person_detail')


class CurrentPersonDetailView(DetailView):
    """DetailView for the current person logged in
    """

    model = Person

    def get_object(self):
        return self.request.user


    def get_context_data(self, **kwargs):
        context = super(CurrentPersonDetailView, self).get_context_data(**kwargs)
        context['transaction_list'] = self.object.get_transactions()
        context['balance_dict'] = self.object.get_balance_by_currencies()
        return context


class CurrentPersonTransactionList(ListView):
    """ListView of the transactions for the current person logged in
    """

    model = Transaction


    def get_queryset(self):
       return self.request.user.get_transactions().order_by('-datetime')


class RegistrationView(_RegistrationView):
    def get_success_url(self,  request,  user):
        """
        Override the default redirect url to index page instead of the default
        one, /users/<username>/
        """
        return ('index', (), {})
