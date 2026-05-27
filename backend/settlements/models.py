from django.db import models


class BondOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SETTLED = "settled", "Settled"
        FAILED = "failed", "Failed"

    investor_wallet = models.CharField(max_length=42)
    issuer_wallet = models.CharField(max_length=42)
    bond_symbol = models.CharField(max_length=32, default="BOND2027")
    quantity = models.PositiveIntegerField(default=1)
    price_per_bond = models.DecimalField(max_digits=18, decimal_places=2, default=1000)
    stablecoin_symbol = models.CharField(max_length=16, default="FAKEUR")
    transaction_hash = models.CharField(max_length=66, blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return self.quantity * self.price_per_bond

    def __str__(self):
        return f"{self.quantity} {self.bond_symbol} for {self.investor_wallet}"
