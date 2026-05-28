from django.db import models


class Bond(models.Model):
    symbol = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)
    isin = models.CharField(max_length=12, blank=True)
    issuer_name = models.CharField(max_length=120)
    issuer_wallet = models.CharField(max_length=42)
    face_value = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")
    coupon_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    maturity_date = models.DateField()
    total_supply = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"
