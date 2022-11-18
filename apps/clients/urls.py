from django.urls import path
from apps.clients.views import ClientListView, ClientDetailView, ClientView, ClientBudgetCreateView

urlpatterns = [
    path('', ClientListView.as_view(), name="clients"),
    path('add/', ClientView.as_view(), name="clients-add"),
    path('<int:pk>/', ClientDetailView.as_view(), name="clients-detail"),
    path('<int:pk>/budget/', ClientBudgetCreateView.as_view(), name="clients-add-budget"),
]
