from django import forms

from books.models import Address, AnonymousAddress


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["customer", 'created_at']

class AnonymousAddressForm(forms.ModelForm):
    class Meta:
        model=AnonymousAddress
        exclude=['session_key', 'created_at']