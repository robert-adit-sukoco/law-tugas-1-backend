from django.db import models
from django.utils.text import slugify
import random
import string
from custom_auth.models import CustomUser


def generate_random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


# Create your models here.
class Article(models.Model):
    slug = models.SlugField(unique=True, primary_key=True, default='', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(default='Article Title', unique=False, max_length=40, null=False)
    content = models.TextField(blank=False)
    published_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            random_number = generate_random_string()
            self.slug = f"{slug}-{random_number}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title