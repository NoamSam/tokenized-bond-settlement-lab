from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from settlements.iso20022 import build_camt054_settlement_message
from settlements.models import (
    Bond,
    BondOrder,
    Investor,
    SettlementMessage,
    SettlementTransaction,
)


class Command(BaseCommand):
    help = "Create demo tokenized bond settlement data for local development."

    def handle(self, *args, **options):
        investor, investor_created = Investor.objects.update_or_create(
            wallet_address="0x1111111111111111111111111111111111111111",
            defaults={
                "display_name": "Alice Investor",
                "email": "alice@example.com",
                "kyc_status": Investor.KycStatus.VERIFIED,
            },
        )

        bond, bond_created = Bond.objects.update_or_create(
            symbol="BOND2027",
            defaults={
                "name": "Tokenized EUR Bond 2027",
                "isin": "FR001400ABC1",
                "issuer_name": "Demo Issuer",
                "issuer_wallet": "0x2222222222222222222222222222222222222222",
                "face_value": Decimal("1000.00"),
                "currency": "EUR",
                "coupon_rate": Decimal("3.50"),
                "maturity_date": "2027-12-31",
                "total_supply": 1000,
            },
        )

        order, order_created = BondOrder.objects.update_or_create(
            investor=investor,
            bond=bond,
            defaults={
                "quantity": 2,
                "price_per_bond": bond.face_value,
                "stablecoin_symbol": "FAKEUR",
                "status": BondOrder.Status.SETTLED,
            },
        )

        transaction, transaction_created = (
            SettlementTransaction.objects.update_or_create(
                order=order,
                defaults={
                    "chain": SettlementTransaction.Chain.LOCAL_ETHEREUM,
                    "transaction_hash": (
                        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    ),
                    "status": SettlementTransaction.Status.CONFIRMED,
                    "block_number": 123,
                    "gas_used": 21000,
                    "settled_at": timezone.now(),
                },
            )
        )
        message_id = f"CAMT054-TX-{transaction.id}"
        message, message_created = SettlementMessage.objects.update_or_create(
            settlement_transaction=transaction,
            defaults={
                "message_type": SettlementMessage.MessageType.CAMT_054,
                "message_id": message_id,
                "xml_payload": build_camt054_settlement_message(
                    transaction,
                    message_id,
                ),
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data ready: "
                f"investor={investor.id} "
                f"({'created' if investor_created else 'updated'}), "
                f"bond={bond.id} ({'created' if bond_created else 'updated'}), "
                f"order={order.id} ({'created' if order_created else 'updated'}), "
                f"transaction={transaction.id} "
                f"({'created' if transaction_created else 'updated'}), "
                f"message={message.id} ({'created' if message_created else 'updated'})."
            )
        )
