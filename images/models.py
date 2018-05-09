from django.db import models
from mlm_builder.basemodel import BaseModel
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from landing.models import Landing


def set_image_name(instanse, filename):
    name = get_random_string(20)
    ext = filename.split('.')[-1]
    path = 'images/{}__{}.{}'.format(instanse.pk, name, ext)
    return path


class UserImage(BaseModel):
    """
    Пользовательские вирусные картинки
    """
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(verbose_name='Изображение', upload_to=set_image_name)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    landing = models.ManyToManyField(
        Landing, verbose_name='Лендинги', through='LandingImage', through_fields=('userimage', 'langing')
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.title

    @property
    def count_landings(self):
        return self.landing.count()

    def get_landingimages(self):
        landingimages = LandingImage.objects.filter(
            userimage=self,
        )
        return landingimages


class LandingImage(BaseModel):
    langing = models.ForeignKey(Landing, on_delete=models.CASCADE)
    userimage = models.ForeignKey(UserImage, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    email_counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} - {}'.format(self.langing, self.userimage)
