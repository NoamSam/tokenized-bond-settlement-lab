from django.contrib import admin

from .models import BondOrder


@admin.register(BondOrder)
class BondOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'investor_wallet',
        'bond_symbol',
        'quantity',
        'status',
        'created_at',
    )
    list_filter = ('status', 'bond_symbol', 'stablecoin_symbol')
    search_fields = ('investor_wallet', 'issuer_wallet', 'transaction_hash')
