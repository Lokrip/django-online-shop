from django.shortcuts import render
from django.views.generic import View


class PaymentIndexView(View):
    def get(self, request):
        return render(request, 'payment/index.html')