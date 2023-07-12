from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    code_of_confirm = models.CharField(max_length=3, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.code_of_confirm)
