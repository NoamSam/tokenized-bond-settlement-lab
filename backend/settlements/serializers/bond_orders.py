from rest_framework import serializers

from settlements.models import Bond, BondOrder, Investor

from .bonds import BondSerializer
from .investors import InvestorSerializer


class BondOrderSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(
        queryset=Investor.objects.all(),
        allow_null=False,
        required=True,
    )
    investor_detail = InvestorSerializer(source="investor", read_only=True)
    bond = serializers.PrimaryKeyRelatedField(
        queryset=Bond.objects.all(),
        allow_null=False,
        required=True,
    )
    bond_detail = BondSerializer(source="bond", read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = BondOrder
        fields = [
            "id",
            "investor",
            "investor_detail",
            "bond",
            "bond_detail",
            "quantity",
            "price_per_bond",
            "stablecoin_symbol",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "total_amount"]

    def validate(self, attrs):
        bond = attrs.get("bond") or getattr(self.instance, "bond", None)
        price_per_bond = attrs.get("price_per_bond")

        if price_per_bond is None and bond is not None:
            attrs["price_per_bond"] = bond.face_value

        return attrs
