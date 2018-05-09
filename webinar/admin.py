from django.contrib import admin
from .models import Webinar, WebinarUser


@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_moderate', 'created')


@admin.register(WebinarUser)
class WebinarUserAdmin(admin.ModelAdmin):
    list_display = ('owner', 'webinar', 'email', 'code', 'is_visit', 'landing', 'created')
    readonly_fields = ('code',)
