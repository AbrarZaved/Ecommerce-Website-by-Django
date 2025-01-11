from django import forms

from authentication.models import Addressbook, Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone_number", "gender"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter Email"}
            ),
            "gender": forms.Select(
                attrs={"class": "form-control", "placeholder": "Select Gender"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Phone Number"}
            ),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Addressbook
        fields = ["division", "city", "zone", "address", "address_label"]
        widgets = {
            "division": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "zone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "address_label": forms.Select(attrs={"class": "form-control"}),
        }
