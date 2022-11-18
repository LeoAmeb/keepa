from django.urls import path
from apps.products.views import ProductListView, ProductView, ProductDetailView, \
                                ProductEntryListView, ProductEntryCreateView, ProductEntryUpdateView, \
                                ProductEntryDetailView, ProductEntryApproveUpdateView

urlpatterns = [
    # Products
    path('', ProductListView.as_view(), name="products"),
    path('add/', ProductView.as_view(), name="products-add"),
    path('<int:pk>/', ProductDetailView.as_view(), name="products-detail"),

    # Products Entries
    path('products-entries/', ProductEntryListView.as_view(), name="product-entry-list"),
    path('products-entries/add/', ProductEntryCreateView.as_view(), name="product-entry-add"),
    path('products-entries/<int:pk>/', ProductEntryDetailView.as_view(), name="product-entry-detail"),
    path('products-entries/<int:pk>/edit/', ProductEntryUpdateView.as_view(), name="product-entry-edit"),
    path('products-entries/<int:pk>/approve/', ProductEntryApproveUpdateView.as_view(), name="product-entry-approve"),
    # path('products-entries/<int:pk>/reject/', ProductentryReject.as_view(), name="product-entry-reject"),
]
