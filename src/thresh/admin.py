from thresh.models import Proposal, Person, Pledge, Transaction
from django.contrib import admin


class PledgeInline(admin.TabularInline):
    model = Pledge
    extra = 1


class ProposalInline(admin.TabularInline):
    model = Proposal
    extra = 1


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1



class ProposalAdmin(admin.ModelAdmin):
    inlines = [PledgeInline]
    list_display = ('title', 'description', 'threshold', 'created', 'expires', 
                    'creator', 'currency')
    list_filter = ['currency', 'creator']
    search_fields = ['title', 'description', 'threshold', 
                    'creator', 'currency']


class PledgeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'created', 
                    'proposal', 'person')
    list_filter = ['proposal', 'person']
    search_fileds = ['amount', 'proposal', 'person']


class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', )
    list_filter = []
    search_fields = ['username']
    fieldsets = [
                ('',
                    {'fields':  ['username', 'email']
                     }
                 ),
    ]
    inlines = [PledgeInline, ProposalInline, TransactionInline]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'datetime', 
                    'currency', 'person', 'pledge')
    list_filter = ['currency', 'person', 'pledge']
    search_fields = ['description', 'amount', 'person', 'pledge']


admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Pledge, PledgeAdmin)
admin.site.register(Transaction, TransactionAdmin)
