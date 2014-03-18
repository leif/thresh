from django.db import models
from django.contrib.auth.models import User

class Person(User):
    def get_balance(self):
        return sum( tx.amount for tx in self.transaction_set.all() )

class Proposal(models.Model):
    title       = models.CharField(max_length=48)
    description = models.CharField(max_length=200)
    creator     = models.ForeignKey(Person)
    threshold   = models.IntegerField()
    created     = models.DateTimeField('date created', auto_now_add=True)
    expires     = models.DateTimeField('expiration date', null=True, blank=True)
    
    def get_percent_backed(self):
        return sum( pledge.amount for pledge in self.pledge_set.all() if pledge.is_backed() ) / float( self.threshold )

class Pledge(models.Model):
    proposal = models.ForeignKey(Proposal)
    person   = models.ForeignKey(Person)
    amount   = models.IntegerField()
    created  = models.DateTimeField('date created')

    def is_backed(self):
        return self.amount <= self.person.get_balance()

class Transaction(models.Model):
    person      = models.ForeignKey(Person)
    amount      = models.IntegerField()
    description = models.CharField(max_length=200)
    datetime    = models.DateTimeField('date')
    pledge      = models.ForeignKey(Pledge, null=True)

