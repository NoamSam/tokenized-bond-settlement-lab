from rest_framework import generics
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from settlements.models import SettlementTransaction
from settlements.serializers import SettlementTransactionSerializer


class SettlementTransactionListCreateView(
    ListModelMixin,
    CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = SettlementTransaction.objects.select_related(
        "order",
        "order__bond",
        "order__investor",
    ).order_by("-created_at")
    serializer_class = SettlementTransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SettlementTransactionDetailView(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = SettlementTransaction.objects.select_related(
        "order",
        "order__bond",
        "order__investor",
    )
    serializer_class = SettlementTransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
