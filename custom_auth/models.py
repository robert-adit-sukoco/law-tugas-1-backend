from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, primary_key=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

# class UserStats(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     articles_posted = models.IntegerField(default=0)
#     reviews_posted = models.IntegerField(default=0)
