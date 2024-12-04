import requests

from .search import Search

from django.http import HttpRequest
from django.shortcuts import redirect

from settings.context.context_processors import get_header_settings

from models.models import Product


class MixinsStore:
    def __init__(self, active_title, menu) -> None:
        self.active_title = active_title
        self.menu = menu
    
    def _search_page(self, request, query):
        query=query.lower()
        MENU_O = get_header_settings(request)['navbarHeader']
        
        for menu in MENU_O:
            if query in menu['title'].lower():
                return redirect(menu['url'])
            
        return None
        
    def search(self, model, query):
        searchClass = Search(model, query)
        return searchClass.search()
    
    def _get_sort(self, sort, queryset):
        if sort == 'price':
            queryset = queryset.order_by(sort)
        elif sort == '-price':
            queryset = queryset.order_by(sort)
        
        return queryset
    
    def _get_filter(
        self, 
        queryset, 
        slug_category, 
        color, prices, 
        product_tag,
        sort
    ):
        if slug_category: 
            queryset = queryset.filter(category__slug=slug_category)

        if color: 
            queryset = queryset.filter(color__name=color)
        
        if product_tag: 
            queryset = queryset.filter(tag__name=product_tag)
            
        
        if prices and prices != 'All': 
            try:
                correct_price = [float(p) for p in prices.split('-')]
                if len(correct_price) == 2:
                    queryset = queryset.filter(price__range=[correct_price[0], correct_price[1]])
                else:
                    queryset = queryset.filter(price__gte=correct_price[-1])
            except ValueError:
                pass
            
        return queryset
        
    def get_queryset_mixins(self, request: HttpRequest, slug_category=None):
        queryset = Product.objects.select_related('category').prefetch_related('color')
        
        color = request.GET.get('color')
        prices = request.GET.get('prices')
        product_tag = request.GET.get('product-tags')
        sort = request.GET.get('sort')
        
        queryset = self._get_filter(
            queryset,
            slug_category, 
            color,
            prices,
            product_tag,
            sort
        )
        
        queryset = self._get_sort(sort, queryset)

        return queryset.order_by('-pk') if not sort else queryset
    
    def set_active_menu(self):
        for item in self.menu:
            item['is_active'] = item['title'] == self.active_title

    def get_menu(self):
        return self.menu
    
    
    
def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_region(ip):
    response = requests.get(f'https://ipinfo.io/{ip}/json')
    data = response.json()
    return data