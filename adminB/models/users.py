from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.core.validators import EmailValidator
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

from cities_light.models import Country
from django_countries.fields import CountryField


def _is_valid_email(email, *args, **kwargs):
    validator = EmailValidator()
    try:
        validator(email)
    except ValidationError:
        raise ValidationError(_('Invalid email format.'))
    
    return True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Менеджер для пользовательской модели User с аутентификацией через email вместо username.

        Args:
            email (string): Email address
            password (string, None): password user

        Returns:
            _type_: _description_
            
        """
        
        if not email:
            raise ValueError(_(
                'The Email field must be set'
            ))
        
        try:
            _is_valid_email(email)
        except ValidationError as e:
            raise ValidationError(_('Неверный формат электронной почты: %s') % e)
        
        email = self.normalize_email(email)
        
        user = self.model(
            email=email, 
            **extra_fields
            )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Call create_user instead of create_superuser
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """User AbstractUser Model

    Args:
        AbstractUser (Model): Create model

    Returns:
        fields: in this model the fields of the model are stored
    """
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(
        _('user description')
    )
    image = models.ImageField(
        _('image for the recipient'),
        upload_to='user/images/%Y/%m/%d/',
        blank=True,
        null=True
    )
    position = models.CharField(
        _('position'),
        max_length=120, 
        default='programmer', 
        blank=True
    )
    date_of_birth = models.DateField(
        _('Date of Birth'), 
        blank=True, 
        null=True
    )
    location = CountryField(verbose_name=_('Country'), blank=True, null=True)
    phone = models.CharField(_('phone number'), max_length=15, unique=True, blank=True, null=True)
    is_author = models.BooleanField(_('author'), default=False)
    is_subscriber = models.BooleanField(_('author'), default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    @property
    def avatar(self):
        try:
            image = self.image.url
        except:
            image = static('store/images/avatar-01.jpg')
        
        return image
    
    def __str__(self) -> str:
        return self.email
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']
    
class GenerateCodeConfirmationEmail(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    
    code = models.CharField(
        max_length=6, 
        verbose_name=_('Confirmation Code'),
        help_text=_('A 6-digit confirmation code')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    expiry_time = models.DateTimeField(
        verbose_name=_('Expiry Time'),
        default=timezone.now() + timedelta(minutes=10) #текущее время создание + 10 минут
    )
    
    def __str__(self):
        return f'Confirmation code for {self.user}'
    
    class Meta:
        verbose_name = _('Confirmation Email Code')
        verbose_name_plural = _('Confirmation Email Codes')
