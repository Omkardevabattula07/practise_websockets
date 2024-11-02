from django.db import models
# from django.utlis import timezone
# Create your models here.

class Message (models.Model):
    room_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    content = models.TextField()
    # timestamp = models.DateTimeField(default=timezone.now)