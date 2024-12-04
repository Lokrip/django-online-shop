from adminB.celery import app
from django.http import HttpRequest

from .service import send


@app.task
def send_spam_email(user_id):
    from models.models import User
    user = User.objects.get(id=user_id)
    send(user)