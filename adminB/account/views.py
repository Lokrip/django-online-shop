from django.views.generic import View
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .service import send
from .tasks import send_spam_email

from models.models import GenerateCodeConfirmationEmail

from .forms import (
    LoginAuthenticationForm,
    SignUpForm,
    EmailConfirmationForm
)

class LoginView(View):
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
            raise Http404("Страница не найдена")
        
        form = LoginAuthenticationForm()
        context = {
            'title': 'Авторизация',
            'form': form
        }
        return render(request, 'account/login.html', context)
    
    def post(self, request):    
        if request.user.is_authenticated:
            raise Http404("Страница не найдена")
        
        form = LoginAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('product:product-home')
            else:
                messages.error(request, 'Пользовтеля с такой почтой существует')
        else:
            messages.error(request, 'Что-то пошло не так')
        
        context = {
            'title': 'Произошла ошибка!',
            'form': form
        }
        return render(request, 'account/login.html', context)

class SignUpView(View):
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
        context = {
            'title': 'Регистрация',
            'form': SignUpForm()
        }
        return render(request, 'account/register.html', context)
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_spam_email.delay(user.id)
            return redirect('account:confirm-email')
        else:
            messages.error(request, form.errors)

        context = {
            'title': 'Ошибка!',
            'form': form
        }
        return render(request, 'account/register.html', context)




class ConfirmEmailCodeView(View):
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
        context = {
            'title': 'Confirm Email Code',
            'form': EmailConfirmationForm()
        }
        return render(request, 'account/email/confirm_email_code.html', context)

    def post(self, request):
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']

            try:
                confirm_data = GenerateCodeConfirmationEmail.objects.get(code=code)
                confirm_data.user.is_active = True
                
                confirm_data.user.save()
                
                login(request, confirm_data.user)
                
                confirm_data.delete()
                
                return redirect('product:product-home')
            except GenerateCodeConfirmationEmail.DoesNotExist:
                messages.error(request, "Неверный код подтверждения.")
        
        messages.error(request, "Произошла ошибка при подтверждении кода.")
        return redirect('account:confirm-email')
            
            
def logout_user(request):
    logout(request)
    return redirect('account:login')