import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advert.settings')

app = Celery('advert')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()