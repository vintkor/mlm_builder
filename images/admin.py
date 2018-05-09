from django.contrib import admin
from .models import UserImage, LandingImage


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    pass


@admin.register(LandingImage)
class LandingImageAdmin(admin.ModelAdmin):
    list_display = (
        'langing',
        'title',
        'email_counter',
    )
    readonly_fields = ('email_counter',)
