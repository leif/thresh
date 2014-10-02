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
    def get_reached_threshold(self, obj):
        return obj.reached_threshold()
    get_reached_threshold.allow_tags = True
    get_reached_threshold.short_description = 'reached threshold'


    inlines = [PledgeInline]
    list_display = ('title', 'description', 'threshold', 'currency', 'creator',
                    'get_reached_threshold', 'created', 'expires', 'creator')
    list_filter = ['currency', 'creator']
    search_fields = ['title', 'description', 'threshold',
                    'creator', 'currency']


class PledgeAdmin(admin.ModelAdmin):
    def get_proposal_currency(self, obj):
        return obj.get_proposal_currency()
    get_proposal_currency.allow_tags = True
    get_proposal_currency.short_description = 'currency'
    list_display = ('amount', 'get_proposal_currency', 'person', 'proposal',
                    'created')
    list_filter = ['proposal', 'person', 'proposal__currency']
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
    list_display = ('description', 'amount', 'currency', 'person', 'pledge',
                    'datetime')
    list_filter = ['currency', 'person', 'pledge']
    search_fields = ['description', 'amount', 'person', 'pledge']


admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Pledge, PledgeAdmin)
admin.site.register(Transaction, TransactionAdmin)
