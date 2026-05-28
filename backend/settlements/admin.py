from django.contrib import admin

from .models import Bond, BondOrder, Investor, SettlementTransaction


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ("id", "display_name", "wallet_address", "kyc_status", "created_at")
    list_filter = ("kyc_status",)
    search_fields = ("display_name", "wallet_address", "email")


@admin.register(Bond)
class BondAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "symbol",
        "issuer_name",
        "face_value",
        "currency",
        "maturity_date",
        "total_supply",
    )
    list_filter = ("currency", "issuer_name")
    search_fields = ("symbol", "name", "isin", "issuer_name", "issuer_wallet")


@admin.register(BondOrder)
class BondOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "investor",
        "bond",
        "quantity",
        "status",
        "created_at",
    )
    list_filter = ("status", "stablecoin_symbol")
    search_fields = (
        "investor__display_name",
        "investor__wallet_address",
        "bond__symbol",
        "bond__name",
    )


@admin.register(SettlementTransaction)
class SettlementTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "chain",
        "transaction_hash",
        "status",
        "block_number",
        "created_at",
    )
    list_filter = ("chain", "status")
    search_fields = ("transaction_hash", "order__bond__symbol")
