from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager

#FIXME: logging settings
import logging
logger = logging.getLogger(__name__)

class Currency(models.Model):
    code   = models.CharField(max_length=3, unique=True)
    name   = models.CharField(max_length=20, unique=True)
    def __unicode__(self):
        return self.name


class Person(AbstractUser):

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


class Proposal(models.Model):
    title       = models.CharField(max_length=48, unique=True)
    description = models.CharField(max_length=200)
    creator     = models.ForeignKey(Person, editable=False)
    threshold   = models.IntegerField()
    currency    = models.ForeignKey(Currency, default=1)
    created     = models.DateTimeField('date created', auto_now_add=True)
    expires     = models.DateTimeField('expiration date', null=True, blank=True)


    # FIXME: all these functions aren't needed, change backed name
    def pledge_amount(self):
        return  sum( pledge.amount for pledge in self.pledge_set.all())


    def get_percent_backed(self):
        return sum( pledge.amount for pledge in self.pledge_set.all() if pledge.is_backed() ) / float( self.threshold )


    def is_backed(self):
        return self.pledge_amount() >=  self.threshold


    def is_gonna_be_backed(self,  amount):
        return self.pledge_amount() + amount >=  self.threshold


    def is_gonna_be_backed_by(self,  amount):
        return self.pledge_amount() + amount -  self.threshold


    def needs_amount_to_be_backed(self):
        return self.threshold - self.pledge_amount()


class Pledge(models.Model):
    proposal = models.ForeignKey(Proposal)
    person   = models.ForeignKey(Person)
    amount   = models.IntegerField()
    created  = models.DateTimeField('date created', auto_now_add=True)


    def is_backed(self):
        return self.amount <= self.person.get_balance(self.proposal.currency)


    def proposal_is_backed(self):
        return self.proposal.is_backed()


class Transaction(models.Model):
    person      = models.ForeignKey(Person, editable=False)
    amount      = models.IntegerField()
    currency    = models.ForeignKey(Currency, default=1)
    description = models.CharField(max_length=200, null=True, blank=True)
    datetime    = models.DateTimeField('date', auto_now_add=True)
    pledge      = models.ForeignKey(Pledge, null=True, blank=True)

