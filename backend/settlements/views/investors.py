from rest_framework import generics
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from settlements.models import Investor
from settlements.serializers import InvestorSerializer


class InvestorListCreateView(
    ListModelMixin,
    CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Investor.objects.order_by("-created_at")
    serializer_class = InvestorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class InvestorDetailView(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
