from django import forms
from django.core.exceptions import ValidationError
from apps.authentication.models import User
from apps.clients.models import Budget, Client


class ClientForm(forms.Form):
    """Forms to create an client"""
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-alternative',}
        )
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-alternative',}
        )
    )

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-alternative',}
        )
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-alternative',}
        )
    )

    budget = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control form-control-alternative',}
        )
    )
 
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already exists.')
        return email


class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = [
            "client",
            "amount"
        ]

        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control form-control-alternative", "autocomplete": False}),
        }

    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop('client_id')
        super().__init__(*args, **kwargs)
        self.fields["client"] = forms.ModelChoiceField(
            queryset=Client.objects.filter(id=client_id),
            empty_label=None,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    def clean_field(self):
        data = self.cleaned_data["field"]
        return data
    
    def clean(self):
        client = self.cleaned_data.get('client')
        amount = self.cleaned_data.get('amount')
        
        budget = client.budgets.last()
        amount += budget.amount
        self.cleaned_data.update({'amount': amount})
        return self.cleaned_data
    