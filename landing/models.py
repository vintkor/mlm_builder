from django.db import models
from mlm_builder.basemodel import BaseModel
from django.contrib.auth.models import User
from django.shortcuts import reverse
from webinar.models import Webinar, WebinarUser
from django.utils.crypto import get_random_string


def set_code():
    """
    Генерация уникального кода для шаблона
    :return: str
    """
    last = Template.objects.first()
    if last is None:
        new_code = 'THEME-1'
    else:
        last_code = last.code.split('-')
        new_code = '{}-{}'.format(last_code[0], (int(last_code[1]) + 1))
    return new_code


def set_image_name(instanse, filename):
    name = get_random_string(20)
    ext = filename.split('.')[-1]
    path = 'lendings/{}__{}.{}'.format(instanse.pk, name, ext)
    return path


class Landing(BaseModel):
    """
    Лендинг привязаный к вебинару
    """
    title = models.CharField(verbose_name='Название', blank=True, null=True, max_length=250)
    description = models.CharField(verbose_name='Описание', blank=True, null=True, max_length=250)
    image = models.ImageField(verbose_name='Изображение', upload_to=set_image_name, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, verbose_name='Вебинар')
    landing_HTML = models.TextField(verbose_name='HTML код лендинга', blank=True, null=True)

    class Meta:
        verbose_name = 'Лендинг'
        verbose_name_plural = 'Лендинги'

    def __str__(self):
        if self.title:
            return self.title
        return '{} > {}'.format(self.owner, self.webinar)

    def get_absolute_url(self):
        return reverse('webinar-view', kwargs={'pk': self.id, 'webinar_slug': self.webinar.slug})

    def get_edit_premium_link(self):
        return reverse('landing:edit-premium', kwargs={'pk': self.id})

    def get_count_email(self):
        """
        Получает количество email собранных этим лендингом
        :return: int
        """
        return WebinarUser.objects.filter(landing=self).count()

    def get_userimages(self):
        from images.models import LandingImage
        userimages = LandingImage.objects.select_related(
            'userimage',
        ).filter(
            langing=self,
        )
        return userimages
