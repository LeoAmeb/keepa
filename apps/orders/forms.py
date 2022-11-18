from django import forms
from django.core.exceptions import ValidationError
from apps.orders.models import Order
from apps.clients.models import Budget, Purchase

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product_entry',]

        widgets = {
            'product_entry': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Product Entry', 'hidden': True}),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'order',
            'client',
            'quantity',
            'amount'
        ]

        widgets = {
            'order': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Order'}),
            'client': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Client'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'onchange': 'onChange();'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
        }

    def clean_client(self):
        client = self.cleaned_data.get("client")
        budgets = client.budgets.all()
        if not budgets:
            raise ValidationError("The client dont have a budget")
        return client
    
    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        client = cleaned_data.get("client")
        budget = client.budgets.last()
        if amount > budget.amount:
            raise ValidationError("The client does not have enough budget: ${}".format(budget.amount))
        return cleaned_data
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order"].disabled = True
        # self.fields["amount"].disabled = True
