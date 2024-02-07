from django.db import models
from django.utils import timezone


# Create your models here.
class ChatModel(models.Model):
    userinput=models.TextField(null=False)
    time=models.DateTimeField(default= timezone.now)