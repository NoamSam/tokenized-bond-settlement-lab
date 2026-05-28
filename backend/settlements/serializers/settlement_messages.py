from rest_framework import serializers

from settlements.iso20022 import build_camt054_settlement_message
from settlements.models import SettlementMessage

from .settlement_transactions import SettlementTransactionSerializer


class SettlementMessageSerializer(serializers.ModelSerializer):
    settlement_transaction_detail = SettlementTransactionSerializer(
        source="settlement_transaction",
        read_only=True,
    )

    class Meta:
        model = SettlementMessage
        fields = [
            "id",
            "settlement_transaction",
            "settlement_transaction_detail",
            "message_type",
            "message_id",
            "xml_payload",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "message_id",
            "xml_payload",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        settlement_transaction = validated_data["settlement_transaction"]
        message_type = validated_data.get(
            "message_type",
            SettlementMessage.MessageType.CAMT_054,
        )
        message_id = f"CAMT054-TX-{settlement_transaction.id}"
        xml_payload = build_camt054_settlement_message(
            settlement_transaction,
            message_id,
        )

        message, _created = SettlementMessage.objects.update_or_create(
            settlement_transaction=settlement_transaction,
            defaults={
                "message_type": message_type,
                "message_id": message_id,
                "xml_payload": xml_payload,
            },
        )
        return message
