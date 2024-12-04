"""
All URLs for this application 
are stored here
"""
from django.urls import path
from . import views
from . import api


""""
"app_name" is the name that Django needs in 
the URL that will chronize the child 
element"""

app_name = 'cart'

urlpatterns = [
     path('basket/', views.CartView.as_view(), name='basket'),
     path('checkout/', views.CheckOutView.as_view(), name='checkout'),
     path('checkout/success/', views.CheckOutSuccsess.as_view(), name='checkout-success'),
     path('checkout/fail/', views.CheckOutFail.as_view(), name='checkout-fail'),
     
     #api
     path('api/v1/cart-add/', api.AddCartApiView.as_view(), name='cart-add'),
     path('api/v1/quantity-add/', api.AddQuantityCartItems.as_view(), name='quantity-cart-add')
]
