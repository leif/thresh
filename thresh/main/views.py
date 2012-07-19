from django.template import Context
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from thresh.main.models import Proposal

class ProposalForm( ModelForm ):
    class Meta:
        model = Proposal

def index(request):
    proposals = Proposal.objects.all().order_by('-created')
    c = Context( dict(
        proposals       = proposals,
        creationForm    = ProposalForm()
        ) )
    c.update(csrf(request))
    return render_to_response( 'index.html', c )

def create(request):
    form = ProposalForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    else:
        c = Context( dict( creationForm = form ) )
        c.update(csrf(request))
        return render_to_response( 'create.html', c )

