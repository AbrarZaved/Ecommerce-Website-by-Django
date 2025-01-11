from django import forms

from authentication.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        Model = Customer
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "phone_number": forms.HiddenInput(),
            "home_address": forms.TextInput(attrs={"class": "form-control"}),
            "office_address": forms.TextInput(attrs={"class": "form-control"}),
        }
