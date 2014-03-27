from django.forms import ModelForm,  HiddenInput,  ValidationError

from thresh.main.models import Pledge

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

    # FIXME: find better way to validate is_backed
    # can't use is_backed here as the pledge object isn't created yet
    # and this'll raise validation errors before is created
    def clean(self):
        cleaned_data = super(PledgeForm, self).clean()
        person = cleaned_data.get("person")
        amount = cleaned_data.get("amount")
        proposal = cleaned_data.get('proposal')
        if not pledge_is_backed(amount,  person,  proposal):        
            raise ValidationError("Insufficient balance, "
                    "pledge with an smaller amount up to your current balance (%s) "
                    "or add more balance to your account."
                    % person.get_balance(proposal.currency))

