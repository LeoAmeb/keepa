from django import forms
import django_filters
from django_filters import filters
from apps.clients.models import Client

class ClientFilter(django_filters.FilterSet):
    first_name = filters.CharFilter(
        field_name="user__first_name",
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'First Name'
            }
        )
    )
    
    last_name = filters.ChoiceFilter(
        field_name="user__last_name",
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }
        )
    )

    class Meta:
        model = Client
        fields = [
            'user'
        ]
