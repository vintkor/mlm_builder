from django.contrib import admin
from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_price', 'get_max_webinars', 'get_max_lending_to_webinar',)
