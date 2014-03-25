from django.template import Context
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render, redirect

from registration.backends.simple.views import RegistrationView \
    as _RegistrationView

from thresh.main.models import Proposal


class ProposalForm( ModelForm ):
    class Meta:
        model = Proposal

def index(request):
    proposals = Proposal.objects.all().order_by('-created')
    return render(request, 'index.html', dict(
        proposals       = proposals,
        creationForm    = ProposalForm()
        ))

def create(request):
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = ProposalForm()
    return render( request, 'create.html', dict( creationForm = form ) )


class RegistrationView(_RegistrationView):
    def get_success_url(self,  request,  user):
        """
        Override the default redirect url to index page instead of the default
        one, /users/<username>/
        """
        return ('index', (), {})
