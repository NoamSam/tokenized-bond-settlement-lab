from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BondOrderApiTests(APITestCase):
    def test_create_bond_order(self):
        response = self.client.post(
            reverse("bond-order-list"),
            {
                "investor_wallet": "0x1111111111111111111111111111111111111111",
                "issuer_wallet": "0x2222222222222222222222222222222222222222",
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["bond_symbol"], "BOND2027")
        self.assertEqual(response.data["stablecoin_symbol"], "FAKEUR")
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(response.data["total_amount"], "2000.00")

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
