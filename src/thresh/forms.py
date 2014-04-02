from django.forms import ModelForm,  HiddenInput,  ValidationError

from thresh.models import Pledge,  Transaction

import logging
logger = logging.getLogger('thresh')


# FIXME: this function is already in models.Pledge, but is redefined here as
# pledge object still doesn't exist in PledgeForm.clean
def pledge_is_backed(amount,  person,  proposal):
    return amount <= person.get_balance(proposal.currency)

class PledgeForm(ModelForm):

    class Meta:
        model = Pledge
        widgets = {
            'proposal': HiddenInput(),
            'person': HiddenInput()
        }


    def clean(self):
        cleaned_data = super(PledgeForm, self).clean()
        person = cleaned_data.get("person")
        amount = cleaned_data.get("amount")
        proposal = cleaned_data.get('proposal')

        #FIXME: add transaction_create url when balance is not enough
        if not pledge_is_backed(amount,  person,  proposal):        
            raise ValidationError("Insufficient balance, "
                    "pledge with an smaller amount up to your current balance "
                    "(%s) or add more balance to your account."
                    % person.get_balance(proposal.currency))

        needs_amount_to_reach_threshold = \
            proposal.needs_amount_to_reach_threshold()
        if amount > needs_amount_to_reach_threshold:
            raise ValidationError(
                "This proposal only needs %s %s to reach the threshold."
                "Pledge with an amount that is <= than %s" % \
                (
                    needs_amount_to_reach_threshold, 
                    proposal.currency.code,
                    needs_amount_to_reach_threshold))


class CurrentPersonTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ('pledge', 'description')

