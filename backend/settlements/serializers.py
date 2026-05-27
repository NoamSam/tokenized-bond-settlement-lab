from rest_framework import serializers

from .models import BondOrder


class BondOrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = BondOrder
        fields = [
            'id',
            'investor_wallet',
            'issuer_wallet',
            'bond_symbol',
            'quantity',
            'price_per_bond',
            'stablecoin_symbol',
            'transaction_hash',
            'status',
            'total_amount',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_amount']
