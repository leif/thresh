from django.forms import ModelForm,  HiddenInput,  ValidationError

from thresh.main.models import Pledge,  Transaction

#FIXME: logging settings
import logging
logger = logging.getLogger(__name__)

def pledge_is_backed(amount,  person,  proposal):
    return amount <= person.get_balance(proposal.currency)

class PledgeForm(ModelForm):

    class Meta:
        model = Pledge
        widgets = {
            'proposal': HiddenInput(),
            'person': HiddenInput()
        }

    # FIXME
    def clean(self):
        cleaned_data = super(PledgeForm, self).clean()
        person = cleaned_data.get("person")
        amount = cleaned_data.get("amount")
        proposal = cleaned_data.get('proposal')
        if not pledge_is_backed(amount,  person,  proposal):        
            raise ValidationError("Insufficient balance, "
                    "pledge with an smaller amount up to your current balance "
                    "(%s) or add more balance to your account."
                    % person.get_balance(proposal.currency))
        # FIXME
        backed = proposal.is_gonna_be_backed_by(amount)
        if backed > 0:
            raise ValidationError("Proposal is gonna be backed by %s %s."
                    "Pledge with %s" % (backed, 
                                      proposal.currency.code, 
                                      proposal.needs_amount_to_be_backed() ))


class CurrentPersonTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ('pledge', 'description')

