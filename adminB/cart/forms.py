from django import forms 

from models.models import (
    ShippingAdress,
)
from django_countries.widgets import CountrySelectWidget

class ShippingAdressForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'stext-111 cl8 plh3 size-111 p-lr-15',
            'placeholder': 'State /  country'
        }
    ))
    
    zip_code = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'stext-111 cl8 plh3 size-111 p-lr-15',
            'placeholder': 'Postcode / Zip'
        }
    ))
    
    
    class Meta:
        model = ShippingAdress
        fields = ['country', 'city', 'zip_code']
        widgets = {
            'country': forms.Select(
                attrs={
                    'class': 'js-select2'
                }
            )
        }

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = ShippingAdress
        exclude = ('user',)
        widgets = {
            'street_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address'
            }),
            'apartment_addres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apartment Address'
            }),
            'country': CountrySelectWidget(attrs={
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ZIP Code'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].choices = [("", 'Select a country')] + list(self.fields['country'].choices)[1:]