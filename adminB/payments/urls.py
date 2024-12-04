"""
All URLs for this application 
are stored here
"""
from django.urls import path, include
from . import views

""""
"app_name" is the name that Django needs in 
the URL that will chronize the child 
element"""

app_name = 'payments'

urlpatterns = [
    path('vs', views.PaymentIndexView.as_view(), name='index')
]
