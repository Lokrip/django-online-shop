from django.contrib import admin

from django.urls.resolvers import URLResolver
from django.utils.html import format_html

from .models import *


admin.site.register(Categories)
admin.site.register(TagModel)
admin.site.register(Brand)
admin.site.register(Supplier)
admin.site.register(ColorModel)
admin.site.register(Product)
admin.site.register(ProductImageModel)
admin.site.register(ShippingAdress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductReview)
admin.site.register(User)
admin.site.register(GenerateCodeConfirmationEmail)