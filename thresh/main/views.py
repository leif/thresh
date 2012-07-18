from django.template import Context, loader
from django.http import HttpResponse
from thresh.main.models import Proposal

def home(request):
    proposals = Proposal.objects.all().order_by('-created')
    t = loader.get_template('proposal_list.html')
    c = Context( dict( proposals = proposals ) )
    return HttpResponse( t.render( c ) )
