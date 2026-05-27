from django.urls import path

from .views import BondOrderDetailView, BondOrderListCreateView

urlpatterns = [
    path("bond-orders/", BondOrderListCreateView.as_view(), name="bond-order-list"),
    path(
        "bond-orders/<int:pk>/", BondOrderDetailView.as_view(), name="bond-order-detail"
    ),
]
