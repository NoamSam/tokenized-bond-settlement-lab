from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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

    def test_create_bond_order_from_investor_and_bond(self):
        order = self.create_order()

        self.assertEqual(order["bond_detail"]["symbol"], "BOND2027")
        self.assertEqual(order["investor_detail"]["kyc_status"], "verified")
        self.assertEqual(order["status"], "pending")
        self.assertEqual(order["total_amount"], "2000.00")

    def test_create_settlement_transaction_for_order(self):
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
        self.assertEqual(response.data["order_detail"]["id"], order["id"])
        self.assertEqual(response.data["chain"], "local_ethereum")
        self.assertEqual(response.data["status"], "confirmed")

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
