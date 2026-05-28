from rest_framework import serializers

from settlements.models import Investor


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
