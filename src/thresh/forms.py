from django.forms import ModelForm,  HiddenInput,  ValidationError
from django.utils.translation import ugettext_lazy as _

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
            raise ValidationError(_("Insufficient balance, "
                    "pledge with an smaller amount up to your current balance "
                    "(%(balance)s) or add more balance to your account."),
                    code='insufficient balance', 
                    params={'balance': person.get_balance(proposal.currency)},
                    )

        needed_amount = \
            proposal.update_pledge_needs_amount_to_reach_threshold(person)
        if amount > needed_amount:
            raise ValidationError(
                _("This proposal only needs %(needed_amount)s %(currency)s to reach the threshold."
                "Pledge with an amount that is <= than %(needed_amount)s"), 
                code='amount will exceed threshold', 
                params={'needed_amount': needed_amount, 
                        'currency': proposal.currency.code},
                )
        return cleaned_data


class CurrentPersonTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ('pledge', 'description')

