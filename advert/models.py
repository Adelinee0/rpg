from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




CATEGORY_CHOICES = [
        ('tanks', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('kvest', 'Квестигверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('alchemist', 'Мастера заклинаний'),
    ]

class Advert(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, default='dd')
    title = models.CharField(max_length=50)
    text = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)

    def preview(self):
        return self.text[0:124] + '...'
    def __str__(self):
        return f'{self.title}: {self.text[:20]}'
    def get_absolute_url(self):
        return reverse('advert_detail', args=[str(self.id)])
        #для того, чтобы после создания объявы кидало на страничку с этой объявой


class Response(models.Model):

    text = models.TextField()
    advertResponse = models.ForeignKey(Advert, on_delete=models.CASCADE)
    authorResponse = models.ForeignKey(User, on_delete=models.CASCADE) # self.request.user
    status = models.BooleanField(default=False)
    createDate = models.DateTimeField(auto_now_add=True)
    #для отслеживания: принят или отклонен отклик




