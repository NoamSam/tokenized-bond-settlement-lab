from rest_framework import serializers

from settlements.models import Bond


class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = [
            "id",
            "symbol",
            "name",
            "isin",
            "issuer_name",
            "issuer_wallet",
            "face_value",
            "currency",
            "coupon_rate",
            "maturity_date",
            "total_supply",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
