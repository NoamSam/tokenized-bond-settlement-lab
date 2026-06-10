from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from settlements.iso20022 import build_camt054_settlement_message
from settlements.models import (
    BondOrder,
    SettlementMessage,
    SettlementTransaction,
)


class Command(BaseCommand):
    help = (
        "Record an on-chain DvP settlement against an existing bond order: "
        "stores the transaction, marks the order as settled, and generates "
        "the camt.054 settlement message. Typically fed with the JSON output "
        "of `npx hardhat run scripts/settle-demo.js` from the chain/ project."
    )

    def add_arguments(self, parser):
        parser.add_argument("--order-id", type=int, required=True)
        parser.add_argument("--tx-hash", type=str, required=True)
        parser.add_argument("--block-number", type=int, required=True)
        parser.add_argument("--gas-used", type=int, default=None)
        parser.add_argument(
            "--chain",
            type=str,
            default=SettlementTransaction.Chain.LOCAL_ETHEREUM,
            choices=[choice[0] for choice in SettlementTransaction.Chain.choices],
        )

    def handle(self, *args, **options):
        try:
            order = BondOrder.objects.select_related("bond", "investor").get(
                pk=options["order_id"]
            )
        except BondOrder.DoesNotExist as exc:
            raise CommandError(
                f"BondOrder {options['order_id']} does not exist."
            ) from exc

        if order.bond is None or order.investor is None:
            raise CommandError(
                f"BondOrder {order.pk} must have a bond and an investor "
                "before it can be settled."
            )

        transaction, _ = SettlementTransaction.objects.update_or_create(
            order=order,
            defaults={
                "chain": options["chain"],
                "transaction_hash": options["tx_hash"],
                "status": SettlementTransaction.Status.CONFIRMED,
                "block_number": options["block_number"],
                "gas_used": options["gas_used"],
                "settled_at": timezone.now(),
            },
        )

        message_id = f"CAMT054-TX-{transaction.id}"
        SettlementMessage.objects.update_or_create(
            settlement_transaction=transaction,
            defaults={
                "message_type": SettlementMessage.MessageType.CAMT_054,
                "message_id": message_id,
                "xml_payload": build_camt054_settlement_message(
                    transaction, message_id
                ),
            },
        )

        order.status = BondOrder.Status.SETTLED
        order.save(update_fields=["status", "updated_at"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Order {order.pk} settled on {transaction.chain} "
                f"(tx {transaction.transaction_hash}, "
                f"block {transaction.block_number}); "
                f"{message_id} generated."
            )
        )
