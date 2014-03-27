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

class Proposal(models.Model):
    title       = models.CharField(max_length=48, unique=True)
    description = models.CharField(max_length=200)
    creator     = models.ForeignKey(Person, editable=False)
    threshold   = models.IntegerField()
    currency    = models.ForeignKey(Currency, default=1)
    created     = models.DateTimeField('date created', auto_now_add=True)
    expires     = models.DateTimeField('expiration date', null=True, blank=True)

    def get_percent_backed(self):
        return sum( pledge.amount for pledge in self.pledge_set.all() if pledge.is_backed() ) / float( self.threshold )


class Pledge(models.Model):
    proposal = models.ForeignKey(Proposal)
    person   = models.ForeignKey(Person)
    amount   = models.IntegerField()
    created  = models.DateTimeField('date created', auto_now_add=True)

    def is_backed(self):
        return self.amount <= self.person.get_balance(self.proposal.currency)

class Transaction(models.Model):
    person      = models.ForeignKey(Person)
    amount      = models.IntegerField()
    currency    = models.ForeignKey(Currency)
    description = models.CharField(max_length=200)
    datetime    = models.DateTimeField('date')
    pledge      = models.ForeignKey(Pledge, null=True)

