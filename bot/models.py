from django.db import models
from django.utils import timezone


class ChatModel(models.Model):
    chathistory = models.JSONField(null=False)
    session_key=models.TextField(null=False)
    time = models.DateTimeField(default=timezone.now)

