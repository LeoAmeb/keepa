from django.urls import path
from apps.orders.views import OrderListView, OrderDetailView, PurchaseCreateView, DeletePurchaseView, BoughtPurchaseView


urlpatterns = [
    # Orders
    path('', OrderListView.as_view(), name="order-list"),
    path('<int:pk>/', OrderDetailView.as_view(), name="order-detail"),
    path('<int:pk>/purchases/', PurchaseCreateView.as_view(), name="order-asign-purchases"),
    path('<int:pk>/purchases/<int:pk_purchase>/delete/', DeletePurchaseView.as_view(), name="order-delete-purchases"),
    path('<int:pk>/purchases/<int:pk_purchase>/bought/', BoughtPurchaseView.as_view(), name="order-bought-purchases")
]
