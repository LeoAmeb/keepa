from django import forms
from django_filters import CharFilter, FilterSet
from apps.authentication.models import User


class UserFilter(FilterSet):
    email = CharFilter(field_name="email", lookup_expr='icontains', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = CharFilter(field_name="first_name", lookup_expr='icontains', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = CharFilter(field_name="last_name", lookup_expr='icontains', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name'
        ]
