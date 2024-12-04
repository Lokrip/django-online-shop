import uuid

from django.db import models
from .users import User, GenerateCodeConfirmationEmail
from django.utils.text import slugify
from django.urls import reverse
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from mptt.models import (
    MPTTModel, 
    TreeForeignKey
)
from django.core.validators import (
    MinValueValidator, 
    MaxValueValidator
)
from django.db.models import Q
from django.conf import settings

from django_countries.fields import CountryField


class Categories(MPTTModel):
    """
    Represents a hierarchical category model using MPTT for nested categories.

    This model organizes categories into a tree structure with efficient 
    querying of hierarchical data. Categories can have subcategories, useful 
    for organizing products or services.

    Attributes:
        name (str): Unique name of the category, indexed for fast lookup.
        slug (str): URL-friendly version of the name, auto-generated if empty.
        description (str): Optional category description (up to 5000 chars).
        parent (TreeForeignKey): Optional reference to the parent category.
        created_at (datetime): Automatically set when the category is created.
        update_at (datetime): Automatically updates when the category is saved.

    Methods:
        save(*args, **kwargs): Auto-generates slug from name if not provided.

    Returns:
        str: The category name.

    Meta Options:
        MPTTMeta: Orders child nodes by name.
        Meta: Orders categories by name and adds indexes for name and slug.
    """
    
    
    name = models.CharField(
        _('Сategory name'), 
        max_length=50, 
        unique=True, 
        db_index=True
    )
    
    slug = models.SlugField(
        _('Slug category name'), 
        max_length=50, 
        help_text=_('Unique category ID for URL'),
        unique=True,
        blank=True,
    )
    
    description = models.TextField(_('Сategory description'), blank=True, max_length=5000)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['name']
        
    class Meta:
        ordering = ['name']
        
        verbose_name = _('Сategory')
        verbose_name_plural = _('Categories')
        
        indexes = [
            models.Index(fields=['name']), 
            models.Index(fields=['slug'])
        ]
        
class TagModel(models.Model):
    name = models.CharField(
        _('Tag name'), 
        max_length=50, 
        unique=True, 
        db_index=True
    )
    
    slug = models.SlugField(
        _('Slug tag name'), 
        max_length=50, 
        help_text=_('Unique tag ID for URL'),
        unique=True,
        blank=True,
    )
    
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.name
        
    class Meta:
        ordering = ['name']
        
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        
        indexes = [
            models.Index(fields=['name']), 
            models.Index(fields=['slug'])
        ]

class Brand(models.Model):
    """Model representing a brand."""
    name = models.CharField(max_length=100, unique=True)
    
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        
        indexes = [
            models.Index(fields=['name']), 
        ]

class Supplier(models.Model):
    """Model representing a supplier."""
    name = models.CharField(max_length=100, unique=True)
    contact_info = models.CharField(max_length=250, blank=True, null=True)
    
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        
        indexes = [
            models.Index(fields=['name']), 
        ]
        
class ColorModel(models.Model):
    name = models.CharField(
        _('Color name'), 
        max_length=50, 
        unique=True, 
        db_index=True
    )
    
    color_icon = models.ImageField(_('Color image'), upload_to='color/%Y/%m/%d/',)
    hex_code = models.CharField(_('HEX code'), max_length=7)
    
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    def __str__(self) -> str:
        return self.name
        
    class Meta:
        ordering = ['name']
        
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')
        
        indexes = [
            models.Index(fields=['name']), 
        ]
        
class Product(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    
    class Status(models.TextChoices):
        """
        Statuses of international 
        products in the store
        """
        
        IN_STOCK = 'in_stock', _(
            'In Stock'
        ) # В наличии
        OUT_OF_STOCK = 'out_of_stock', _(
            'Out of Stock'
        ) # Нет в наличии
        PRE_ORDER = 'pre_order', _(
            'Pre-order'
        ) # Предзаказ
        COMING_SOON = 'coming_soon', _(
            'Coming Soon'
        ) # Скоро в продаже
        SOLD_OUT = 'sold_out', _(
            'Sold Out'
        ) # Распродано
        AWAITING_RESTOCK = 'awaiting_restock', _(
            'Awaiting Restock'
        ) # Ожидается пополнение
        ON_SALE = 'on_sale', _(
            'On Sale'
        ) # Распродажа
        NEW = 'new', _(
            'New'
        ) # Новинка
        DISCONTINUED = 'discontinued', _(
            'Discontinued'
        ) # Снят с производства
        RESERVED = 'reserved', _(
            'Awaiting Review'
        ) # Зарезервировано (ожидает проверки)
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name=_('product user')
    )
    
    title = models.CharField(
        _('Title product'), 
        max_length=150, 
        db_index=True
    )
    description = models.TextField(_('Description product'), max_length=5000)
    
    price = models.DecimalField(
        _('Price Product'), 
        max_digits=10, 
        decimal_places=2, 
        default=99.99
    )
    
    slug = models.SlugField(
        _('Slug product name'), 
        max_length=50, 
        help_text=_('Unique tag ID for URL'),
        unique=True,
        blank=True,
    )
    sales_count = models.PositiveIntegerField(_('Sales Count'), default=0)
    status = models.CharField(
        _('status'), 
        max_length=30, 
        choices=Status.choices,
        default=Status.RESERVED
    )
    
    discount = models.IntegerField(
        _('Discount (%)'), 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ], 
        default=0
    )
    image = models.ImageField(
        _('Product Image'), 
        upload_to='product/images/%Y/%m/%d/',
        blank=True,
        null=True
    )
    stock = models.PositiveIntegerField(_('Quantity in stock'), default=0)
    summary = models.PositiveIntegerField(_('Total price'), default=0)
    
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name=_('Brand'))
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, verbose_name=_('Supplier'))

    
    color = models.ManyToManyField(ColorModel, verbose_name=_('ManyToManyField to Color'), blank=True)
    tag = models.ManyToManyField(TagModel, verbose_name=_('ManyToManyField to Tag'), blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    @property
    def get_image(self):
        try:
            image = self.image.url
        except:
            image = static('default_images/users/user.png')
        
        return image
    
    @property 
    def related_products(self):
        return Product.objects.filter(Q(category=self.category), ~Q(slug=self.slug))
    
    @property
    def get_images(self):
        return ProductImageModel.objects.filter(product=self)
    
    @property
    def get_review_count(self):
        return ProductReview.objects.filter(product=self).count()
    
    @property
    def get_review(self):
        return ProductReview.objects.filter(product=self).order_by('-pk')
    
    @property
    def get_price(self):
        if self.discount > 0:
            discount_amount = (self.price * self.discount) / 100
            discounted_price = self.price - discount_amount
            return round(discounted_price, 2)
        return self.price
    
    def get_absolute_url(self):
        return reverse('product:store-detail', kwargs={'detail_slug': self.slug})
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['slug']),
        ]

class ProductImageModel(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
        related_name='product_images'
    )
    image = models.ImageField(
        _('Product Image'), 
        upload_to='product/images/%Y/%m/%d/',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    def __str__(self):
        return f'{self.product.title} -> {self.image.url}'

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
   
class ShippingAdress(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name=_('User')
    )      
    street_address = models.CharField(max_length=100, verbose_name=_('адрес улицы'))
    apartment_addres = models.CharField(max_length=100, verbose_name=_('адрес квартиры'))
    
    country = CountryField(verbose_name=_('Country'))
    city = models.CharField(max_length=100, verbose_name=_('город'))
    
    zip_code = models.CharField(max_length=100, verbose_name=_('почтовый индекс'))
    phone = models.CharField(max_length=20, verbose_name=_('номер телефона'))
    
    def __str__(self) -> str:
        return f'User ShippingAdress {
            self.user.username} Zip code {
                self.zip_code}'
    
    class Meta:
        verbose_name = 'Shipping Adress'
        verbose_name_plural = 'Shipping Adress'
    
class Order(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    
    # tax хранится сумма налога, которая рассчитывается на основе стоимости товаров в 
    # заказе, но не вся стоимость с учётом налогов. Это поле хранит только саму сумму 
    # налога, Поле tax в модели заказа представляет собой налог, который 
    # добавляется к общей стоимости заказа. В интернет-магазинах и системах 
    # продаж налог (например, НДС или другой местный налог) 
    # обычно рассчитывается как процент от стоимости товаров 
    # или услуг, и это поле хранит сумму налога для конкретного заказа.
    
    class OrderStatus(models.TextChoices):
        """
        Statuses of orders
        """
        PENDING = 'pending', _(
            'Pending'
        )              # В ожидании
        CONFIRMED = 'confirmed', _(
            'Confirmed'
        )        # Подтвержден
        SHIPPED = 'shipped', _(
            'Shipped'
        )              # Отправлен
        DELIVERED = 'delivered', _(
            'Delivered'
        )        # Доставлен
        CANCELLED = 'cancelled', _(
            'Cancelled'
        )     # Скоро в продаже
    
    customers = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name=_('Customers')
    )
    
    shipping_address = models.ForeignKey(
        ShippingAdress, 
        on_delete=models.CASCADE, 
        verbose_name=_('shipping address'),
        blank=True, null=True
    )
    
    session_token = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        verbose_name=_('Session Token')
    )
    
    order_status = models.CharField(
        max_length=20, 
        choices=OrderStatus.choices, 
        default=OrderStatus.PENDING, 
        verbose_name=_('Order Status')
    )
    
    order_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Order Date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Last Updated'))
    
    total_prices = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Total Price'),
        default=0.00,
    )
    tax = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Tax')
    )
    discount = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00, 
        verbose_name=_('Discount')
    )
    transaction_id = models.CharField(
        _('Transaction ID'),
        max_length=255,
        blank=True,
        null=True,
    )
    
    @property
    def total_price(self):
        orderItems = OrderItem.objects.filter(order=self)
        if orderItems.exists():
            summa = sum(int(item.total_price) for item in orderItems)
        else:
            summa = 0
        return summa
    
    def __str__(self):
        return f"Order {self.id} by {self.customers}"
    
    class Meta:
        unique_together = ('customers',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        
class LikeProduct(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name=_('User')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    liked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    def __str__(self):
        return f"{self.user} liked {self.product}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        verbose_name=_('Order')
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name=_('P   roduct')
    )
    price = models.DecimalField(
        _('Price Product'), 
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    
    def __str__(self):
        return f"Order {self.order.id} by {self.product.id}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        if self.price <= 0:
            self.price = self.total_price
        super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = _('OrderItem')
        verbose_name_plural = _('OrderItems')
        
class ProductReview(MPTTModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name=('product_review')
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name=_('Anime'),
        related_name='product_review'
    )
    email = models.EmailField(_('email address'), null=True, blank=True)
    name = models.CharField(_('name'), max_length=120, db_index=True, null=True, blank=True)
    content = models.TextField(_('comment'), max_length=120)
    parent = TreeForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('parent comment')
    )
    
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    update_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.name} -> {self.user.username} -> {self.anime.title}'
    
    
    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
    