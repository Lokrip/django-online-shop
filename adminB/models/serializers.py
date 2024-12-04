from rest_framework import serializers
from models.models import (
    Product,
    Categories,
    Order,
    OrderItem,
    ProductImageModel
)

from django.contrib.auth import get_user_model

User = get_user_model()

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = ['id', 'image']

class ProductSerializers(serializers.ModelSerializer):
    price_with_discount = serializers.SerializerMethodField()
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    product_images = ProductImagesSerializer(many=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'discount', 'price_with_discount', 
            'image','slug', 'status', 'stock', 'summary', 'brand', 'supplier', 
            'color', 'tag', 'category', 'created_at', 'update_at', 'product_images'
        ]
    
    # Когда вы используете SerializerMethodField, Django REST Framework ожидает, 
    # что вы определите метод в сериализаторе с именем get_<имя_поля>. Этот метод будет 
    # вызываться для каждого объекта, который сериализуется, 
    # и он должен возвращать значение для соответствующего поля.
    def get_price_with_discount(self, obj):
        return obj.get_price
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializers(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'price',
            'quantity',
            'total_price',
            'created_at',
            'update_at'
        ]

class OrderSerializer(serializers.ModelSerializer):
    customers = UserSerializer(read_only=True)
    orderitem_set = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'customers',
            'orderitem_set'
        ]
    
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'