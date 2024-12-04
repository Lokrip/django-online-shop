from django.shortcuts import render
from django.views.generic import View
from models.models import Product

class AdminHome(View):
    def get(self, request):
        products = Product.objects.order_by('-sales_count')[:5]
        print(products)
        context = {
            'products': products
        }
        return render(request, 'admin_home/dashboard.html', context)