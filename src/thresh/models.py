from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager

import logging
logger = logging.getLogger('thresh')

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
                   if pledge.is_backed() ) / float( self.threshold )


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


class Transaction(models.Model):
    person      = models.ForeignKey(Person, editable=False)
    amount      = models.IntegerField()
    currency    = models.ForeignKey(Currency, default=1)
    description = models.CharField(max_length=200, null=True, blank=True)
    datetime    = models.DateTimeField('date', auto_now_add=True)
    pledge      = models.ForeignKey(Pledge, null=True, blank=True)


    def __unicode__(self):
        if self.pledge:
            return '%s %s on %s by %s' % \
            (self.amount, self.currency,  self.pledge, self.person)
        else:
            return '%s %sby %s' % \
                (self.amount, self.currency, self.person)
