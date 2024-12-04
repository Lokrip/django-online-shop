import random

from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from models.users import GenerateCodeConfirmationEmail


from adminB.settings import EMAIL_HOST_USER

def generate_unique_code():
    while True:
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        if not GenerateCodeConfirmationEmail.objects.filter(code=code).exists():
            return code

def send(user):
    ## Задается тема письма, которое будет отправлено пользователю
    subject = 'Confirm Your Email'
    from_email = EMAIL_HOST_USER
    random_numbers = generate_unique_code()
    to = user.email
    
    confirmation = GenerateCodeConfirmationEmail.objects.create(
        user=user,
        code=random_numbers
    )
    
    # render_to_string — это функция из модуля django.template.loader, 
    # которая используется для рендеринга (обработки) HTML-шаблона и преобразования его в строку
    html_content = render_to_string('account/email/confirm_email.html', {
        'random_numbers': random_numbers,
        'title': 'Confirm Email'
    })
    
    # Функция strip_tags в Django используется для удаления всех HTML-тегов из строки, 
    # оставляя только текстовое содержимое. 
    # Это важно, когда вы хотите преобразовать HTML-код в чистый текст.
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    
    # Добавляем HTML-версию как альтернативу
    email.attach_alternative(html_content, 'text/html')
    
    #send отпровляет письмо
    email.send()
    