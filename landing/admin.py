from django.contrib import admin
from .models import Landing


@admin.register(Landing)
class LandingUserWebinarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created',)
