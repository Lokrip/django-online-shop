from django.urls import reverse
from models.models import (
    Order,
    OrderItem,
    ShippingAdress
)


def get_menu(reverse):
    MENU_NAVBAR = [
        {
            'title': 'Home',
            'url': reverse("product:product-home"), 
            'is_active': True,
        },
        {'title': 'Store', 'url': reverse('product:store'), 'is_active': False},
        {'title': 'Create', 'url': reverse('product:product-create'), 'is_active': False},
    ]
    
    return MENU_NAVBAR

def get_filter_price_ranges():
    FILTER_PRICE_RANGES = [
        {'label': 'All', 'href': ''},
        {'label': '$0.00 - $50.00', 'href': ''},
        {'label': '$50.00 - $100.00', 'href': ''},
        {'label': '$100.00 - $150.00', 'href': ''},
        {'label': '$150.00 - $200.00', 'href': ''},
        {'label': '$200.00+', 'href': ''},
    ]
    
    return FILTER_PRICE_RANGES



def get_header_settings(request):
    
    if request.user.is_authenticated:
        try:
            shipping_address  = ShippingAdress.objects.get(user=request.user)  
        except ShippingAdress.DoesNotExist:
            shipping_address  = None
    
        order, created = Order.objects.get_or_create(
            customers=request.user,
            order_status=Order.OrderStatus.PENDING,
            shipping_address=shipping_address 
        )
        orderItems = OrderItem.objects.filter(order=order)
    else:
        order = None
        orderItems = []
        
    menu = get_menu(reverse=reverse)
    filterPriceRanges = get_filter_price_ranges()
    
    context = {
        "navbarHeader": menu,
        "filterPriceRanges": filterPriceRanges,
        "orderItems": orderItems,
        "order": order
    }
    return context
