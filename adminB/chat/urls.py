from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('lobby/', views.LobbyView.as_view(), name='lobby')
]