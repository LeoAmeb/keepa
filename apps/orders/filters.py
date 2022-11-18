from django import forms
import django_filters
from django_filters import filters
from apps.orders.models import Order


class OrderFilter(django_filters.FilterSet):
    asin = filters.CharFilter(field_name="product_entry__product__asin", lookup_expr="iexact", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    
    start_date = filters.DateFilter(field_name="created_at", lookup_expr="gte", widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))
    
    stop_date = filters.DateFilter(field_name="created_at", lookup_expr="lte", widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))

    class Meta:
        model = Order
        fields = [
            "asin",
            "created_at",
        ]
