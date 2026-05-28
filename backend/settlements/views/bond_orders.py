from rest_framework import generics
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from settlements.models import BondOrder
from settlements.serializers import BondOrderSerializer


class BondOrderListCreateView(
    ListModelMixin,
    CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = BondOrder.objects.select_related("bond", "investor").order_by(
        "-created_at"
    )
    serializer_class = BondOrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BondOrderDetailView(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = BondOrder.objects.select_related("bond", "investor")
    serializer_class = BondOrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
