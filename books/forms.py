from django import forms

from books.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["customer", 'created_at']
