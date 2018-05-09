from django.contrib import admin
from .models import Profile
from sorl.thumbnail.admin import AdminImageMixin


@admin.register(Profile)
class ProfileAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = (
        'user',
        'package',
    )
