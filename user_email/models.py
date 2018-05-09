from django.db import models
from mlm_builder.basemodel import BaseModel
from django.contrib.auth.models import User
from webinar.models import Webinar


class Email(BaseModel):
    email = models.EmailField(verbose_name='Email', unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', blank=True,             null=True, related_name='owner_emails')

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        unique_together = ('email', 'owner')

    def __str__(self):
        return self.email
