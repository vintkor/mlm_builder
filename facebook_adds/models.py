from django.db import models
from mlm_builder.basemodel import BaseModel


class FacebookAPI(BaseModel):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    app_id = models.CharField(max_length=200)
    app_secret = models.CharField(max_length=200)
    app_access_token = models.CharField(max_length=200)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
