from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES=(("admin","Admin"),("staff","Staff"),("user","User"))
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default="user")
    
    def __str__(self):
        return f"{self.username} {self.role}"