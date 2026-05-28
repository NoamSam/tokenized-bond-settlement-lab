from django.db import models

from .settlement_transactions import SettlementTransaction


class SettlementMessage(models.Model):
    class MessageType(models.TextChoices):
        CAMT_054 = "camt.054", "camt.054 Bank to Customer Debit/Credit Notification"

    settlement_transaction = models.OneToOneField(
        SettlementTransaction,
        on_delete=models.CASCADE,
        related_name="settlement_message",
    )
    message_type = models.CharField(
        max_length=16,
        choices=MessageType.choices,
        default=MessageType.CAMT_054,
    )
    message_id = models.CharField(max_length=64, unique=True)
    xml_payload = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message_type} {self.message_id}"
