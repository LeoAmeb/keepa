from django import forms
import django_filters
from django_filters import filters
from apps.products.models import Product, ProductEntry


class ProductFilter(django_filters.FilterSet):
    brand = filters.CharFilter(field_name="brand", lookup_expr="icontains", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    
    title = filters.CharFilter(field_name="title", lookup_expr="icontains", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    
    color = filters.CharFilter(field_name="color", lookup_expr="icontains", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    
    asin = filters.CharFilter(field_name="asin", lookup_expr="icontains", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    
    start_date = filters.DateFilter(field_name="created_at", lookup_expr="gte", widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))
    
    stop_date = filters.DateFilter(field_name="created_at", lookup_expr="lte", widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))

    class Meta:
        model = Product
        fields = [
            "brand",
            "title",
            "color",
            "asin",
            "created_at",
        ]


class ProductEntryFilter(django_filters.FilterSet):
    # folio = filters.CharFilter(field_name="folio", lookup_expr="icontains", widget=forms.TextInput(
    #     attrs={"class": "form-control", "placeholder": "Folio"}))
    
    asin = filters.CharFilter(field_name="product__asin", lookup_expr="icontains", widget=forms.TextInput(
        attrs={"class": "form-control"}))

    status = filters.ChoiceFilter(field_name="status", choices=ProductEntry.STATUS_CHOICES, widget=forms.Select(
        attrs={"class": "form-select"}))

    start_date = filters.DateFilter(field_name="created_at", lookup_expr="gte", widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))
    
    stop_date = filters.DateFilter(field_name="created_at", lookup_expr="lte", widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))

    class Meta:
        model = ProductEntry
        fields = [
            # "folio",
            "status",
            "created_at",
            "product__asin",
        ]
