from rest_framework import serializers

from settlements.models import SettlementTransaction

from .bond_orders import BondOrderSerializer


class SettlementTransactionSerializer(serializers.ModelSerializer):
    order_detail = BondOrderSerializer(source="order", read_only=True)

    class Meta:
        model = SettlementTransaction
        fields = [
            "id",
            "order",
            "order_detail",
            "chain",
            "transaction_hash",
            "status",
            "block_number",
            "gas_used",
            "settled_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
