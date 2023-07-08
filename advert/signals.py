from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response


@receiver(post_save, sender=Response)
def response_created(instance,  created, **kwargs):
    if not created:
        return

    send_mail(
        subject='На ваше объявление откликнулись!',
        message=f'{instance.advertResponse.author.username}, вам отклик от {instance.authorResponse}! Вот он: "{instance.text}" ',
        from_email=None,
        recipient_list=[instance.advertResponse.author.email],
    )

@receiver(post_save, sender=Response)
def response_accept(instance, **Kwargs):
    if instance.status:

        send_mail(
        subject='Ваш отклик приняли!',
        message=f'{instance.authorResponse.username}, ваш отклик к "{instance.advertResponse.title}" приняли',
        from_email=None,  #
        recipient_list=[instance.authorResponse.email],
    )