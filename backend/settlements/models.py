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
