from django.urls import path
from . import views

app_name = 'admin_home'

urlpatterns = [
     path('admin-home/', views.AdminHome.as_view(), name='admin-home')
]
