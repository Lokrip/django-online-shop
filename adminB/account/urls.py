"""
All URLs for this application 
are stored here
"""
from django.urls import path
from . import views

""""
"app_name" is the name that Django needs in 
the URL that will chronize the child 
element"""
app_name = 'account'


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('confirm-email/', views.ConfirmEmailCodeView.as_view(), name='confirm-email'),
]


