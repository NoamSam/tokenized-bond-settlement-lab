from django.db import models


class Investor(models.Model):
    class KycStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    display_name = models.CharField(max_length=120)
    wallet_address = models.CharField(max_length=42, unique=True)
    email = models.EmailField(blank=True)
    kyc_status = models.CharField(
        max_length=16,
        choices=KycStatus.choices,
        default=KycStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} ({self.wallet_address})"
