from django import forms
from django.contrib.auth import (
    get_user_model,             
    authenticate
)
from django.core.exceptions import ValidationError
from models.users import GenerateCodeConfirmationEmail

from utils.mixins import is_valid_username

User = get_user_model()

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        "class": 'size-111 bor8 stext-102 cl2 p-lr-20',
    }))
    
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={
        "class": 'size-111 bor8 stext-102 cl2 p-lr-20',
    }))
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": 'size-111 bor8 stext-102 cl2 p-lr-20',
    }))
    
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": 'size-111 bor8 stext-102 cl2 p-lr-20',
    }))
    
    def clean_username(self):
        """
        Validates the provided username and ensures it meets the specified criteria.

        Raises:
            ValidationError: If the username is invalid based on the defined rules.

        Returns:
            str: The validated username.
        """
        username: str = self.cleaned_data.get('username')

        # Проверка на наличие username
        if username is None:
            raise ValidationError("Username is required.")
        
        try:
            is_valid_username(username)
        except ValidationError as fv:
            raise fv
        
        return username
    
    def clean_password2(self):
        """
        Validates that the two provided passwords match.

        Raises:
            ValidationError: If the passwords do not match.

        Returns:
            str: The validated second password.
        """
        
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2
    
    def clean(self):
        """
        Validates the entire form data.

        Checks that all required fields are filled, 
        and that the provided username and email are unique.

        Raises:
            ValidationError: If any required fields are missing or if the username or email already exists.

        Returns:
            dict: The cleaned data from the form.
        """
        cleaned_data = super().clean()
        
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        if not all([email, username]):
            raise ValidationError('All fields are required')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError(f'Username {username} is already taken.')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError(f'Email {email} is already registered.')
        
        return cleaned_data
    
    def save(self, is_email=False):
        """
        Creates and saves a new user instance with the validated data from the form.

        Returns:
            User: The newly created user instance.
        """
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        
        user = User.objects.create_user(
            username=username,
            email=email,
        )
        
        user.set_password(password)
        
        user.is_active = False
        
        user.save()
    
        return user
        

    
class LoginAuthenticationForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={
        "class": 'size-111 bor8 stext-102 cl2 p-lr-20',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": 'size-111 bor8 stext-102 cl2 p-lr-20',
    }))
    
    def clean(self):
        """
        Validates the login credentials (email and password).

        Checks if the provided email and password are valid and authenticates the user.

        Raises:
            ValidationError: If the email or password is incorrect.

        Returns:
            dict: The cleaned data from the form.
        """
        email = self.cleaned_data.get('email')
        password  = self.cleaned_data.get('password')
        
        if email and password:
            self.user = authenticate(
                request=self.request,
                email=email, 
                password=password
            )
            
            if self.user is None:
                raise ValidationError('Неверная электронная почта или пароль')
        
        return self.cleaned_data
    
    def get_user(self):
        """
        Retrieves the authenticated user instance.

        Returns:
            User: The authenticated user instance, or None if not authenticated.
        """
        return self.user

class EmailConfirmationForm(forms.ModelForm):
    class Meta:
        model = GenerateCodeConfirmationEmail
        fields = ('code',)