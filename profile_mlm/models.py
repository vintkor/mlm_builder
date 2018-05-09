from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from mlm_builder.utils import set_filename
from ckeditor_uploader.fields import RichTextUploadingField
from phonenumber_field.modelfields import PhoneNumberField
from sorl.thumbnail.fields import ImageField
from package.models import Package
from mlm_builder.basemodel import BaseModel
from webinar.models import Webinar
from landing.models import Landing


def set_default_package():
    try:
        return Package.objects.get(is_start_package=True).id
    except Package.DoesNotExist:
        return None


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = ImageField(verbose_name=_('Аватар'), upload_to=set_filename, blank=True, null=True, default=None)
    description = RichTextUploadingField(verbose_name=_('Обо мне'), blank=True, default='')
    is_push_email = models.BooleanField(verbose_name=_('Получать Email уведомления'), default=True)
    website = models.URLField(verbose_name=_('Сайт'), blank=True)
    phone = PhoneNumberField(verbose_name=_('Телефон'), max_length=30, blank=True)
    skype = models.CharField(verbose_name=_('Логин в Skype'), max_length=150, blank=True)

    balance = models.DecimalField(verbose_name='Баланс', max_digits=10, decimal_places=2, default=0)

    link_vkontakte = models.URLField(verbose_name=_('Ссылка на страницу ВКонтакте'), blank=True)
    link_facebook = models.URLField(verbose_name=_('Ссылка на страницу Facebook'), blank=True)
    link_twitter = models.URLField(verbose_name=_('Ссылка на страницу Twitter'), blank=True)
    link_instagram = models.URLField(verbose_name=_('Ссылка на страницу Instagram'), blank=True)
    link_odnoklassniki = models.URLField(verbose_name=_('Ссылка на страницу Одноклассники'), blank=True)
    link_my_world = models.URLField(verbose_name=_('Ссылка на страницу Мой мир'), blank=True)

    package = models.ForeignKey(Package, verbose_name='Тарифный план', on_delete=models.SET_DEFAULT, default=set_default_package, blank=True, null=True)
    package_end_date = models.DateTimeField(verbose_name='Дата окончания тарифа', blank=True, null=True)

    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')

    def __str__(self):
        return self.user.username

    def is_can_create_webinar(self):
        """
        Проверка может ли пользователь добавлять новые вебинары
        :return: bool
        """
        if self.package is None:
            return False

        exist_webinars_count = Webinar.objects.filter(owner=self.user).count()
        webinar_limit = self.package.max_webinars

        if webinar_limit > exist_webinars_count or webinar_limit == -1:
            return True
        return False

    def is_can_create_lending_to_webinar(self, webinar):
        """
        Проверка может ли пользователь добавлять новые дендинги к вебинарам
        :return: bool
        """
        if self.package is None:
            return False

        exist_landing_to_webinar_count = Landing.objects.filter(
            owner=self.user,
            webinar=webinar,
        ).count()
        lendings_limit = self.package.max_lending_to_webinar

        if lendings_limit > exist_landing_to_webinar_count or lendings_limit == -1:
            return True
        return False

    def is_can_create_premium_template(self):
        return self.package.can_create_premium_template


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
