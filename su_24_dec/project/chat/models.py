
# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)