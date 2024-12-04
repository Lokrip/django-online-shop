from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

import stripe


from models.models import (
    Order, 
    OrderItem,
    ShippingAdress,
    Product
)
from .forms import (
    ShippingAdressForm,
    CheckOutForm
)

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

class CartView(View):
    """_summary_

    Args:
        View (View All Request): [
            GET,
            POST,
            PUT, 
            PATCH,
            DELETE
        ]
    """
    
    def get(self, request):
        if request.user.is_authenticated:
            shipping = ShippingAdress.objects.filter(user=request.user).first()
            form_shipping = ShippingAdressForm(instance=shipping)
                
            order, created = Order.objects.get_or_create(
                customers=request.user,
                order_status=Order.OrderStatus.PENDING,
                defaults={
                   'shipping_address': None,
                   'total_prices': 0.00,
                   'tax': 0.00,
                   'discount': 0.00,
                }
            )
            
            order_items = OrderItem.objects.filter(order=order)
        else:
            form_shipping = ShippingAdressForm()
            order_items = []
            order = None
            
        context = {
            'title': 'Корзина товаров',
            'order': order,
            'order_items': order_items,
            'form_shipping': form_shipping
        }
        return render(request, 'cart/shoping-cart.html', context)

class CheckOutView(LoginRequiredMixin,View):
    """_summary_

    Args:
        View (View All Request): [
            GET,
            POST,
            PUT, 
            PATCH,
            DELETE
        ]
    """
    
    def get(self, request):
        form = CheckOutForm()
        context = {
            'title': 'CheckOut',
            'form': form
        }
        return render(request, 'cart/checkout.html', context)
    
    
    def post(self, request):
        if request.user.is_authenticated:
            form = CheckOutForm(request.POST)
            
            if form.is_valid():
                shipping_adress, created_shipping_adress = ShippingAdress.objects.get_or_create(
                    user=request.user,
                    defaults=form.cleaned_data
                )
                
                order, created_order = Order.objects.get_or_create(
                    customers=request.user, 
                    order_status=Order.OrderStatus.PENDING,
                    defaults={
                        'shipping_address': shipping_adress,
                        'total_prices': 0.00,
                        'tax': 0.00,
                        'discount': 0.00,
                    }
                )

                if order and shipping_adress:
                    order_Items = OrderItem.objects.filter(order=order)
                    
                    session_data = {
                        'mode': 'payment',
                        'success_url': request.build_absolute_uri(reverse('cart:checkout-success')),
                        'cancel_url': request.build_absolute_uri(reverse('cart:checkout-fail')),
                        'line_items': [],
                        'client_reference_id': order.id,
                    }

                    
                    for order_Item in order_Items:
                        product = Product.objects.get(pk=order_Item.product.pk)
                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(order_Item.price) * 100,
                                'currency': 'usd',
                                'product_data': {
                                    'name': product
                                }
                            },
                            'quantity': order_Item.quantity 
                        })
                        
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)
            else:
                messages.error(request, 'Форма не валидна попробуйте еще раз')
                
            context = {
                'title': 'Ошибка!',
                'form': form
            }
            return render(request, 'cart/checkout.html', context)
                    

class CheckOutSuccsess(View):
    """_summary_

    Args:
        View (View All Request): [
            GET,
            POST,
            PUT, 
            PATCH,
            DELETE
        ]
    """
    
    def get(self, request):
        return render(request, 'cart/success.html')
    
class CheckOutFail(View):
    """_summary_

    Args:
        View (View All Request): [
            GET,
            POST,
            PUT, 
            PATCH,
            DELETE
        ]
    """
    
    def get(self, request):
        return render(request, 'cart/fail.html')
        
        