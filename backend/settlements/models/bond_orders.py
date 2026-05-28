from django.db import models

from .bonds import Bond
from .investors import Investor


class BondOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SETTLEMENT_SUBMITTED = "settlement_submitted", "Settlement submitted"
        SETTLED = "settled", "Settled"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    investor = models.ForeignKey(
        Investor,
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
        blank=True,
    )
    bond = models.ForeignKey(
        Bond,
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    price_per_bond = models.DecimalField(max_digits=18, decimal_places=2, default=1000)
    stablecoin_symbol = models.CharField(max_length=16, default="FAKEUR")
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return self.quantity * self.price_per_bond

    def __str__(self):
        bond_symbol = self.bond.symbol if self.bond else "unassigned bond"
        investor = (
            self.investor.wallet_address if self.investor else "unassigned investor"
        )
        return f"{self.quantity} {bond_symbol} for {investor}"
