from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)