from django.db import models
from mlm_builder.basemodel import BaseModel
from mlm_builder.utils import set_filename, slugify
from django.contrib.auth.models import User
from .validators import youtube_validator
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField
import datetime
from django.shortcuts import reverse
from django.utils.crypto import get_random_string


def get_unique_code():
    code = get_random_string(8)
    exist_count = WebinarUser.objects.filter(code=code).count()
    if exist_count > 0:
        return get_unique_code()
    return code


# TODO Написать свой валидатор для Vimeo
class Webinar(BaseModel):
    """
    Модель вебинара
    """
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=None)
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг', blank=True, null=True)
    description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)
    video = models.URLField(verbose_name='Видео', validators=[youtube_validator])
    image = ImageField(verbose_name='Изображение', upload_to=set_filename, blank=True, null=True)
    author = models.CharField(verbose_name='Автор', max_length=100, blank=True, null=True)
    active_start_date = models.DateTimeField(verbose_name='Дата старта показа')
    active_end_date = models.DateTimeField(verbose_name='Дата прекращения показа')
    is_moderate = models.BooleanField(default=False, verbose_name='Одобренно модератором')

    class Meta:
        verbose_name = 'Вебинар'
        verbose_name_plural = 'Вебинары'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('webinar:detail', kwargs={'slug': self.slug, 'owner_pk': self.owner.id})

    def get_video_id(self):
        from urllib.parse import urlparse
        url_data = urlparse(self.video).query
        for param in url_data.split('&'):
            if param.split('=')[0] == 'v':
                return param.split('=')[1]

    def is_webinar_active_now(self):
        """
        Проверяет доступность вебинара на момент запроса 
        :return: bool
        """
        now = datetime.datetime.now()
        if (
            self.active_start_date <= now
            and self.active_end_date >= now
            and self.is_moderate
        ):
            return True
        return False

    def make_unique_slug(self):
        """
        Генерация уникального СЛАГа
        """
        new_slug = slugify(self.title)
        count = 0
        while Webinar.objects.filter(slug=new_slug).exclude(id=self.id).count() > 0:
            count += 1
            new_slug = '{slug}-{count}'.format(slug=new_slug, count=count)
        self.slug = new_slug

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.make_unique_slug()
        return super(Webinar, self).save(*args, **kwargs)


class WebinarUser(BaseModel):
    """
    Модель посетителя который подписался на вебинар через конкретный лендинг
    """
    owner = models.ForeignKey(User, on_delete=None, verbose_name='Пользователь')
    webinar = models.ForeignKey(Webinar, on_delete=None, verbose_name='Вебинар')
    email = models.EmailField(verbose_name='E-mail')
    landing = models.ForeignKey('landing.Landing', on_delete=models.SET_DEFAULT, verbose_name='Ленгинг',            default=None, blank=True, null=True)
    code = models.CharField(max_length=8, verbose_name='Код', default=get_unique_code, unique=True)
    is_visit = models.BooleanField(default=False, verbose_name='Посещал вебинар')

    class Meta:
        verbose_name = 'Пользователи вебинара'
        verbose_name_plural = 'Пользователи вебинара'

    def __str__(self):
        return self.email
