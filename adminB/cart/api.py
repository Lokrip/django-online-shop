from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from models.models import (
    Product,
    Order,
    OrderItem,
    ShippingAdress
)
from models.serializers import OrderSerializer

class AddCartApiView(APIView):
    def post(self, request):
        data = request.data
        
        productId = data.get('productId', None)
        method = data.get('method', None)
        payload = data.get('productCount', None)
        
        if data is None or 'productId' not in data:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            shipping, _ = ShippingAdress.objects.get_or_create(user=request.user)   
            product = Product.objects.get(id=productId)
                
            # Atomic: Самый часто используемый декоратор и менеджер контекста — transaction.atomic. 
            # Он позволяет обернуть часть кода в транзакцию. Если в этом блоке произойдет исключение, 
            # все изменения в базе данных будут отменены. Пример
            with transaction.atomic():
                order, created = Order.objects.get_or_create(
                    customers=request.user,
                    order_status=Order.OrderStatus.PENDING,
                    shipping_address=shipping
                )
                
                order_item, item_created = OrderItem.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={
                        'quantity': payload, 
                        'price': product.get_price
                    }
                )
                
                if not item_created:
                    order_item.quantity += (int(payload) or 1) if method == 'add' else -(int(payload) or 1)
                    if order_item.quantity <= 0:
                        order_item.delete()
                    else:
                        order_item.price = order_item.quantity * product.get_price
                        order_item.save()
                    order_item.price = order_item.quantity * product.get_price
                    order_item.save()
                
                order.total_prices = sum(item.price for item in order.orderitem_set.all())
                order.save()
                
            serializers = OrderSerializer(order)
                
            return Response(serializers.data, status=status.HTTP_201_CREATED)
                
        except Product.DoesNotExist:
            return Response(
                {'error': f'product with this ID {productId} is out of stock'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ShippingAdress.DoesNotExist:
            return Response(
                {'error': f'ShippingAdress not found!'},
                status=status.HTTP_404_NOT_FOUND
            )


class AddQuantityCartItems(APIView):
    def post(self, request):
        data = request.data
        
        method = data.get('method', None)
        payload = data.get('payload', None)
        
        
        