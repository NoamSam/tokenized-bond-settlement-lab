from django.urls import path

from .views import (
    BondDetailView,
    BondListCreateView,
    BondOrderDetailView,
    BondOrderListCreateView,
    InvestorDetailView,
    InvestorListCreateView,
    SettlementMessageDetailView,
    SettlementMessageListCreateView,
    SettlementTransactionDetailView,
    SettlementTransactionListCreateView,
)

urlpatterns = [
    path("investors/", InvestorListCreateView.as_view(), name="investor-list"),
    path("investors/<int:pk>/", InvestorDetailView.as_view(), name="investor-detail"),
    path("bonds/", BondListCreateView.as_view(), name="bond-list"),
    path("bonds/<int:pk>/", BondDetailView.as_view(), name="bond-detail"),
    path("bond-orders/", BondOrderListCreateView.as_view(), name="bond-order-list"),
    path(
        "bond-orders/<int:pk>/", BondOrderDetailView.as_view(), name="bond-order-detail"
    ),
    path(
        "settlement-transactions/",
        SettlementTransactionListCreateView.as_view(),
        name="settlement-transaction-list",
    ),
    path(
        "settlement-transactions/<int:pk>/",
        SettlementTransactionDetailView.as_view(),
        name="settlement-transaction-detail",
    ),
    path(
        "settlement-messages/",
        SettlementMessageListCreateView.as_view(),
        name="settlement-message-list",
    ),
    path(
        "settlement-messages/<int:pk>/",
        SettlementMessageDetailView.as_view(),
        name="settlement-message-detail",
    ),
]
