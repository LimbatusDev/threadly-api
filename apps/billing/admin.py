from django.contrib import admin

from . import models


@admin.register(models.BillingConfig)
class BillingConfigAdmin(admin.ModelAdmin):
    list_display = ('price_monthly', 'price_yearly')


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'amount', 'state')
    list_filter = ['state']
    search_fields = ['number']
