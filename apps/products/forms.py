from django import forms
from django.core.exceptions import ValidationError

from apps.products.utils import get_data_keepa
from apps.products.models import Product, ProductEntry


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["asin", ]
        widgets = {
            "asin": forms.TextInput(attrs={"class": "form-control form-control-alternative"}),
        }

    def clean(self):
        asin = self.data.get("asin")

        product = Product.objects.filter(asin=asin)
        if product:
            product = product.last()
            if not product.is_available():
                raise ValidationError({"asin": "Is not possible create a request of this product."})

        succes, response = get_data_keepa(asin)
        if not succes:
            raise ValidationError(response)
        else:
            self.cleaned_data.update({"title": response["title"]})
            self.cleaned_data.update({"brand": response["brand"]})
            self.cleaned_data.update({"description": response["description"]})
            self.cleaned_data.update({"size": response["size"]})
            self.cleaned_data.update({"color": response["color"]})
            self.cleaned_data.update({"image": response["imagesCSV"].split(",")[0]})
            self.cleaned_data.update({"last_price_buy_box": response["data"]["NEW"][-1]})
            self.cleaned_data.update({"json_keepa": response})

        return self.cleaned_data

    def save(self, commit=True):
        product, created = Product.objects.update_or_create(
            asin=self.cleaned_data.get("asin"),
            defaults={
                "title":self.cleaned_data.get("title"),
                "brand":self.cleaned_data.get("brand"),
                "description":self.cleaned_data.get("description"),
                "size":self.cleaned_data.get("size"),
                "color":self.cleaned_data.get("color"),
                "image":self.cleaned_data.get("image"),
                "last_price_buy_box":self.cleaned_data.get("last_price_buy_box"),
                "json_keepa":self.cleaned_data.get("json_keepa"),
            }
        )
        return product, created


class ProductEntryCreateForm(forms.ModelForm):
    """Form tu create a Product Entry"""
    class Meta:
        model = ProductEntry
        fields = [
            "store",
            "link_store",
            "buy_amount_per_piece",
            "observations",
            "quantity"
        ]

        widgets = {
            "store": forms.TextInput(attrs={"class": "form-control form-control-alternative"}),
            "link_store": forms.URLInput(attrs={"class": "form-control form-control-alternative"}),
            "buy_amount_per_piece": forms.NumberInput(attrs={"class": "form-control form-control-alternative"}),
            "observations": forms.TextInput(attrs={"class": "form-control form-control-alternative"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control form-control-alternative"})
        }


class ProductEntryUpdateForm(forms.ModelForm):
    """Form to update a Product Entry"""

    class Meta:
        model = ProductEntry
        fields = [
            "store",
            "link_store",
            "buy_amount_per_piece",
            "observations",
            "quantity"
        ]

        widgets = {
            "store": forms.TextInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Store"}),
            "link_store": forms.URLInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Link store"}),
            "buy_amount_per_piece": forms.NumberInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Buy amount per piece"}),
            "observations": forms.TextInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Observations"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Quantity"})
        }

class ProductEntryApproveForm(forms.ModelForm):

    class Meta:
        model = ProductEntry
        fields = [
            "status",
            "store",
            "link_store",
            "buy_amount_per_piece",
            "observations",
            "quantity"
        ]

        widgets = {
            "status": forms.Select(attrs={"class": "form-control form-control-alternative", "placeholder": "Status", "autocomplete": False}),
            "store": forms.TextInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Store", "autocomplete": False}),
            "link_store": forms.URLInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Link store", "autocomplete": False}),
            "buy_amount_per_piece": forms.NumberInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Buy amount per piece", "autocomplete": False}),
            "observations": forms.TextInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Observations", "autocomplete": False}),
            "quantity": forms.NumberInput(attrs={"class": "form-control form-control-alternative", "placeholder": "Quantity", "autocomplete": False})
        }

