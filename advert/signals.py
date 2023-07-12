from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import mail_response_created, mail_response_accept

from .models import Response


@receiver(post_save, sender=Response)
def response_created(instance,  created, **kwargs):
    if created:
        mail_response_created(instance)



@receiver(post_save, sender=Response)
def response_accept(instance, **Kwargs):
    if instance.status:
        mail_response_accept(instance)

