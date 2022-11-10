from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, PasswordResetForm, SetPasswordForm
from apps.authentication.models import User


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "current-password"}),
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
    }


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "autocomplete": False}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": False}),
        }


class PasswordResetFormCustom(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control"})
    )


class SetPasswordFormCustom(SetPasswordForm):
    new_password1 = forms.CharField(
        label= "New password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label= "New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
    )
