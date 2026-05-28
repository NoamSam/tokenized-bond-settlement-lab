from rest_framework import serializers

from .models import Bond, BondOrder, Investor, SettlementTransaction


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = [
            "id",
            "display_name",
            "wallet_address",
            "email",
            "kyc_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


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
