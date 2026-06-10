from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Bond, BondOrder, Investor, SettlementMessage, SettlementTransaction


class SettlementWorkflowApiTests(APITestCase):
    def create_investor(self):
        response = self.client.post(
            reverse("investor-list"),
            {
                "display_name": "Alice Investor",
                "wallet_address": "0x1111111111111111111111111111111111111111",
                "email": "alice@example.com",
                "kyc_status": "verified",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def create_bond(self):
        response = self.client.post(
            reverse("bond-list"),
            {
                "symbol": "BOND2027",
                "name": "Tokenized EUR Bond 2027",
                "isin": "FR001400ABC1",
                "issuer_name": "Demo Issuer",
                "issuer_wallet": "0x2222222222222222222222222222222222222222",
                "face_value": "1000.00",
                "currency": "EUR",
                "coupon_rate": "3.50",
                "maturity_date": "2027-12-31",
                "total_supply": 1000,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def create_order(self):
        investor = self.create_investor()
        bond = self.create_bond()

        response = self.client.post(
            reverse("bond-order-list"),
            {
                "investor": investor["id"],
                "bond": bond["id"],
                "quantity": 2,
                "stablecoin_symbol": "FAKEUR",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def create_settlement_transaction(self):
        order = self.create_order()

        response = self.client.post(
            reverse("settlement-transaction-list"),
            {
                "order": order["id"],
                "chain": "local_ethereum",
                "transaction_hash": (
                    "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                ),
                "status": "confirmed",
                "block_number": 123,
                "gas_used": 21000,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def test_create_bond_order_from_investor_and_bond(self):
        order = self.create_order()

        self.assertEqual(order["bond_detail"]["symbol"], "BOND2027")
        self.assertEqual(order["investor_detail"]["kyc_status"], "verified")
        self.assertEqual(order["status"], "pending")
        self.assertEqual(order["total_amount"], "2000.00")

    def test_create_settlement_transaction_for_order(self):
        transaction = self.create_settlement_transaction()

        self.assertEqual(
            transaction["order_detail"]["bond_detail"]["symbol"], "BOND2027"
        )
        self.assertEqual(transaction["chain"], "local_ethereum")
        self.assertEqual(transaction["status"], "confirmed")

    def test_generate_iso20022_style_settlement_message(self):
        transaction = self.create_settlement_transaction()

        response = self.client.post(
            reverse("settlement-message-list"),
            {
                "settlement_transaction": transaction["id"],
                "message_type": "camt.054",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message_id"], f"CAMT054-TX-{transaction['id']}")
        self.assertIn("<Document>", response.data["xml_payload"])
        self.assertIn("BOND2027", response.data["xml_payload"])
        self.assertIn(transaction["transaction_hash"], response.data["xml_payload"])

    def test_list_bond_orders_starts_empty(self):
        response = self.client.get(reverse("bond-order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class ApiDocumentationTests(APITestCase):
    def test_openapi_schema_is_available(self):
        response = self.client.get(reverse("schema"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger_ui_is_available(self):
        response = self.client.get(reverse("swagger-ui"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SeedDemoDataCommandTests(APITestCase):
    def test_seed_demo_data_command_creates_demo_workflow(self):
        call_command("seed_demo_data")

        self.assertEqual(Investor.objects.count(), 1)
        self.assertEqual(Bond.objects.count(), 1)
        self.assertEqual(BondOrder.objects.count(), 1)
        self.assertEqual(SettlementTransaction.objects.count(), 1)
        self.assertEqual(SettlementMessage.objects.count(), 1)

        order = BondOrder.objects.select_related("investor", "bond").get()
        self.assertEqual(order.investor.kyc_status, Investor.KycStatus.VERIFIED)
        self.assertEqual(order.bond.symbol, "BOND2027")
        self.assertEqual(order.status, BondOrder.Status.SETTLED)
        self.assertEqual(order.total_amount, 2000)


class RecordOnchainSettlementCommandTests(APITestCase):
    def test_records_transaction_message_and_settles_order(self):
        investor = Investor.objects.create(
            display_name="Alice Investor",
            wallet_address="0x1111111111111111111111111111111111111111",
            kyc_status=Investor.KycStatus.VERIFIED,
        )
        bond = Bond.objects.create(
            symbol="BOND2027",
            name="Tokenized EUR Bond 2027",
            issuer_name="Demo Issuer",
            issuer_wallet="0x2222222222222222222222222222222222222222",
            face_value="1000.00",
            maturity_date="2027-12-31",
            total_supply=1000,
        )
        order = BondOrder.objects.create(investor=investor, bond=bond, quantity=2)

        tx_hash = "0x" + "f" * 64
        call_command(
            "record_onchain_settlement",
            order_id=order.pk,
            tx_hash=tx_hash,
            block_number=7,
            gas_used=111910,
        )

        order.refresh_from_db()
        transaction = SettlementTransaction.objects.get(order=order)
        message = SettlementMessage.objects.get(settlement_transaction=transaction)

        self.assertEqual(order.status, BondOrder.Status.SETTLED)
        self.assertEqual(transaction.status, SettlementTransaction.Status.CONFIRMED)
        self.assertEqual(transaction.transaction_hash, tx_hash)
        self.assertEqual(transaction.block_number, 7)
        self.assertIsNotNone(transaction.settled_at)
        self.assertEqual(message.message_id, f"CAMT054-TX-{transaction.id}")
        self.assertIn(tx_hash, message.xml_payload)

    def test_fails_for_unknown_order(self):
        from django.core.management.base import CommandError

        with self.assertRaises(CommandError):
            call_command(
                "record_onchain_settlement",
                order_id=999,
                tx_hash="0x" + "a" * 64,
                block_number=1,
            )
