from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager
from django.db import transaction

import logging
logger = logging.getLogger('thresh')


@transaction.atomic
def transfer_pledges_to_proposal(proposal):
    # withdraw txs
    for pledge in proposal.get_all_pledges():
        tx = Transaction(person = pledge.person,
                         amount = -pledge.amount,
                         currency = proposal.currency,
                         description = 'withdraw %s %s from %s for %s' %
                            (pledge.amount,
                             proposal.currency,
                             pledge.person,
                             proposal
                            ),
                         pledge = pledge)
        tx.save()
    # deposit tx
    tx = Transaction(person = proposal.creator,
                     amount = proposal.threshold,
                     currency = proposal.currency,
                     description = 'deposit %s %s on %s' %
                        (proposal.threshold,
                         proposal.currency,
                         proposal.title)
                    )
    tx.save()



class Currency(models.Model):
    code   = models.CharField(max_length=3, unique=True)
    name   = models.CharField(max_length=20, unique=True)
    def __unicode__(self):
        return self.name


class Person(AbstractUser):


    def __unicode__(self):
        return self.username


    def get_balance(self, currency):
        return sum( tx.amount for tx in self.transaction_set.filter(currency=currency) )


    def get_balance_by_currencies(self):
        bc = {}
        for currency in Currency.objects.all():
            if self.get_balance(currency):
                bc[currency.code] = self.get_balance(currency)
        return bc


    def get_transactions(self):
        return self.transaction_set.all()


    def get_pledge_on_proposal(self, proposal):
        if self.pledge_set.filter(proposal=proposal):
            return self.pledge_set.filter(proposal=proposal)[0]
        else:
            return None

    def get_pledges(self):
        return self.pledge_set.all()


    def get_pending_pledges(self):
        #return [p for p in self.pledge_set.all()i
        #            if not p.proposal_reached_threshold()]
        return [p for p in self.pledge_set.all()
                    if not p.transaction_set.all()]

    def get_completed_pledges(self):
        #return [p for p in self.pledge_set.all()
        #            if p.proposal_reached_threshold()]
        return [p for p in self.pledge_set.all()
                    if p.transaction_set.all()]


    def get_proposals(self):
        return self.proposal_set.all()


    def get_pending_proposals(self):
        return [p for p in self.proposal_set.all() if not p.reached_threshold()]


    def get_completed_proposals(self):
        return [p for p in self.proposal_set.all() if p.reached_threshold()]


class Proposal(models.Model):
    title       = models.CharField(max_length=48, unique=True)
    description = models.CharField(max_length=200)
    creator     = models.ForeignKey(Person, editable=False)
    threshold   = models.IntegerField()
    currency    = models.ForeignKey(Currency, default=1)
    created     = models.DateTimeField('date created', auto_now_add=True)
    expires     = models.DateTimeField('expiration date', null=True, blank=True)
    # FIXME: might be useful to add completed boolean field, that is set to
    # true when the thershold is reached and the transactions are performed


    def __unicode__(self):
        return self.title


    def get_all_pledges(self):
        return self.pledge_set.all()


    def pledges_total_amount(self):
        return  sum( pledge.amount for pledge in self.get_all_pledges() \
                    if pledge.is_backed())


    def get_percent_backed(self):
        return sum( pledge.amount for pledge in self.get_all_pledges() \
                   if pledge.is_backed() ) * 100 / float( self.threshold )


    # FIXME: find better name for reach(ed) threshold methods => completed?
    # FIXME: we could differenciate reached_threshold from complete with other
    # function that checks that all pledges on the proposal were withdrawed
    # (have transactions)
    # If Transaction would have relation to proposal, we could also check if
    # there was a deposit transaction for the proposal
    # Or just add the boolean completed field
    def reached_threshold(self):
        return self.pledges_total_amount() >=  self.threshold


    def needs_amount_to_reach_threshold(self):
        return self.threshold - self.pledges_total_amount()


    def get_pledge_by_person(self,  person):
        if self.pledge_set.filter(person=person):
            return self.pledge_set.filter(person=person)[0]
        else:
            return None


    # when updating person pledge, the previous pledge amount by that person
    # shouldn't be considered
    def pledges_amount_without_person_pledge(self, person):
        return  sum( pledge.amount for pledge in self.get_all_pledges() \
                    if pledge.is_backed() and pledge.person != person)


    def update_pledge_needs_amount_to_reach_threshold(self, person):
        return self.threshold - \
                self.pledges_amount_without_person_pledge(person)


class Pledge(models.Model):
    proposal = models.ForeignKey(Proposal)
    person   = models.ForeignKey(Person)
    amount   = models.IntegerField()
    created  = models.DateTimeField('date created', auto_now_add=True)
    # FIXME: might be useful to add completed boolean field


    def __unicode__(self):
        return '%s %s on %s by %s' % \
            (self.amount, self.proposal.currency,  self.proposal, self.person)


    def is_backed(self):
        return self.amount <= self.person.get_balance(self.proposal.currency)


    # FIXME: find better name for reach(ed) threshold methods => completed?
    # same comment as for Proposal...
    def proposal_reached_threshold(self):
        return self.proposal.reached_threshold()


    # see comment for previos function
    def is_completed(self):
        if self.transaction_set.all(): return True
        return False


    def get_proposal_currency(self):
        return self.proposal.currency


    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        logger.debug('pledge save')
        logger.debug(self.amount)
        logger.debug(self.proposal.needs_amount_to_reach_threshold())
        if self.proposal.needs_amount_to_reach_threshold() <= self.amount:
            logger.debug('proposal is gonna reach threshold')

        super(Pledge, self).save(
            force_insert, force_update, *args, **kwargs)

        if self.proposal_reached_threshold():
            logger.debug('proposal reached threshold')
            transfer_pledges_to_proposal(self.proposal)


class Transaction(models.Model):
    person      = models.ForeignKey(Person, editable=False)
    amount      = models.IntegerField()
    currency    = models.ForeignKey(Currency, default=1)
    description = models.CharField(max_length=200, null=True, blank=True)
    datetime    = models.DateTimeField('date', auto_now_add=True)
    # FIXME: this could be change to OneToOne
    pledge      = models.ForeignKey(Pledge, null=True, blank=True)
    # FIXME: might be useful to add proposal OneToOne field


    def __unicode__(self):
        if self.pledge:
            return 'pledge: %s' % \
            (self.pledge,)
        else:
            return '%s: %s %s by %s' % \
                (self.description,  self.amount, self.currency, self.person)
