from django.contrib import admin
from .models import FacebookAPI


@admin.register(FacebookAPI)
class FacebookAPIAdmin(admin.ModelAdmin):
    list_display = ('title', 'active',)
