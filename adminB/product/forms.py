from django import forms
from models.models import ProductReview, Product

class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        label='Your review',
        widget=forms.Textarea(
            attrs={
                'class': 'size-110 bor8 stext-102 cl2 p-lr-20 p-tb-10',
            }
        )
    )
    
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20',
            }
        )
    )
    
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20',
            }
        )
    )
    
    
    class Meta:
        model = ProductReview
        fields = (
            'name', 
            'content',
            'email'
        )

class CreatePoroductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['user', 'created_at', 'update_at', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20', 
                'placeholder': 'Enter product title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20', 
                'placeholder': 'Enter product description', 
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20', 
                'placeholder': 'Enter product price'
            }),
            'status': forms.Select(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20'
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20', 
                'placeholder': 'Enter discount percentage'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20', 
                'placeholder': 'Enter stock quantity'
            }),
            'summary': forms.NumberInput(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20', 
                'placeholder': 'Total price'
            }),
            'brand': forms.Select(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20'
            }),
            'supplier': forms.Select(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20'
            }),
            'color': forms.SelectMultiple(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20'
            }),
            'tag': forms.SelectMultiple(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20'
            }),
            'category': forms.Select(attrs={
                'class': 'size-111 bor8 stext-102 cl2 p-lr-20'
            }),
        }