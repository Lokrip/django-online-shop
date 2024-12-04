from django.dispatch import receiver
from django.db.models.signals import post_save

from models.models import Product

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    #sender: Это класс модели, который инициировал сигнал. Например, если сигнал был вызван после сохранения пользователя, sender будет классом User.
    #instance: Это конкретный экземпляр модели Product, который был создан или обновлен. Он содержит все данные этого пользователя.
    #created: Булево значение, указывающее, был ли экземпляр создан (True) или обновлен (False).
    
    if created:
        instance.slug = f"{instance.slug}-{instance.id}"
        instance.save(update_fields=['slug'])
    