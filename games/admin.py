from django.contrib import admin
from .models import *

class GameAdmin(admin.ModelAdmin):
    exclude = ('slug',)


# Register your models here.
admin.site.register(Game, GameAdmin)
admin.site.register(Genre)
admin.site.register(Review)