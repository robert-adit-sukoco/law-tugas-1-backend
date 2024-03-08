from django.contrib import admin
from .models import *

class ArticleAdmin(admin.ModelAdmin):
    exclude = ('slug',)

# Register your models here.
admin.site.register(Article, ArticleAdmin)