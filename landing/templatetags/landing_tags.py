from django import template
from webinar.models import Webinar

register = template.Library()


@register.simple_tag
def get_user_webinars(user):
    return Webinar.objects.filter(owner=user)
