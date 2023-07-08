from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response


@receiver(post_save, sender=Response)
def response_created(instance,  created, **kwargs):
    if not created:
        return

    #email = [instance.advertResponse.author.email],
    #subject = 'На ваше объявление откликнулись!',
    #text_content = (f'{instance.advertResponse.author.username}, вам отклик от {instance.authorResponse}! Вот он: "{instance.text}" '),
    #html_content =html_content = (
       # f'{instance.advertResponse.author.username}<br>'
       # f'Вам отклик от: {instance.authorResponse}<br><br>'
       # f'Вот он: {instance.text}'


   # msg = EmailMultiAlternatives(subject, text_content, None, [email])
   # msg.attach_alternative(html_content, "text/html")
   # msg.send()