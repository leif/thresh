from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager
from django.db import transaction

import logging
logger = logging.getLogger('thresh')


@transaction.atomic
def transfer_pledges_to_proposal(proposal):
    for pledge in proposal.get_all_pledges():
        # withdraw txs
        tx = Transaction(person = pledge.person, 
                         amount = -pledge.amount, 
                         currency = proposal.currency, 
                         description = 'withdraw', 
                         pledge = pledge)
        tx.save()
    # deposit tx
    tx = Transaction(person = proposal.creator, 
                     amount = proposal.threshold, 
                     currency = proposal.currency, 
                     description = 'deposit')
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


class Proposal(models.Model):
    title       = models.CharField(max_length=48, unique=True)
    description = models.CharField(max_length=200)
    creator     = models.ForeignKey(Person, editable=False)
    threshold   = models.IntegerField()
    currency    = models.ForeignKey(Currency, default=1)
    created     = models.DateTimeField('date created', auto_now_add=True)
    expires     = models.DateTimeField('expiration date', null=True, blank=True)


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


    # FIXME: find better name for reach(ed) threshold methods
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


    def __unicode__(self):
        return '%s %s on %s by %s' % \
            (self.amount, self.proposal.currency,  self.proposal, self.person)


    def is_backed(self):
        return self.amount <= self.person.get_balance(self.proposal.currency)


    def proposal_reached_threshold(self):
        return self.proposal.reached_threshold()


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
    pledge      = models.ForeignKey(Pledge, null=True, blank=True)


    def __unicode__(self):
        if self.pledge:
            return '%s: %s %s on pledge %s by %s' % \
            (self.description,  self.amount, self.currency,  self.pledge, 
            self.person)
        else:
            return '%s: %s %s by %s' % \
                (self.description,  self.amount, self.currency, self.person)
