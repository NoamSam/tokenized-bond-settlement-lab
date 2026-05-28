from rest_framework import generics
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)

from settlements.models import SettlementMessage
from settlements.serializers import SettlementMessageSerializer


class SettlementMessageListCreateView(
    ListModelMixin,
    CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = SettlementMessage.objects.select_related(
        "settlement_transaction",
        "settlement_transaction__order",
        "settlement_transaction__order__bond",
        "settlement_transaction__order__investor",
    ).order_by("-created_at")
    serializer_class = SettlementMessageSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SettlementMessageDetailView(
    RetrieveModelMixin,
    DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = SettlementMessage.objects.select_related(
        "settlement_transaction",
        "settlement_transaction__order",
        "settlement_transaction__order__bond",
        "settlement_transaction__order__investor",
    )
    serializer_class = SettlementMessageSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
