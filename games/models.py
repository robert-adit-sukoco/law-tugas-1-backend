from django.db import models
from django.utils.text import slugify
import random
import uuid
import string
from django.core.validators import MaxValueValidator, MinValueValidator
from custom_auth.models import CustomUser


def generate_random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Game(models.Model):
    slug = models.SlugField(unique=True, primary_key=True, default='', blank=True)
    title = models.CharField(default='GameName', unique=False, max_length=100, null=False)
    genre = models.ManyToManyField(Genre)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            random_number = generate_random_string()
            self.slug = f"{slug}-{random_number}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    star = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(default='', max_length=200)
    user_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_fk = models.ForeignKey(Game, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.id}"