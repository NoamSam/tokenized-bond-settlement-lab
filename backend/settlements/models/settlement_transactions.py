from django.db import models

from .bond_orders import BondOrder


class SettlementTransaction(models.Model):
    class Chain(models.TextChoices):
        LOCAL_ETHEREUM = "local_ethereum", "Local Ethereum"
        ETHEREUM = "ethereum", "Ethereum"
        TEZOS = "tezos", "Tezos"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        FAILED = "failed", "Failed"

    order = models.OneToOneField(
        BondOrder,
        on_delete=models.CASCADE,
        related_name="settlement_transaction",
    )
    chain = models.CharField(
        max_length=32,
        choices=Chain.choices,
        default=Chain.LOCAL_ETHEREUM,
    )
    transaction_hash = models.CharField(max_length=128, unique=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    block_number = models.PositiveBigIntegerField(null=True, blank=True)
    gas_used = models.PositiveBigIntegerField(null=True, blank=True)
    settled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chain} {self.transaction_hash}"
