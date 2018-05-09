from django.db import models
from mlm_builder.basemodel import BaseModel
from finance.models import Currency
from django.utils.html import format_html


# TODO is_start_package должен быть только один
class Package(BaseModel):
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    weight = models.PositiveSmallIntegerField(default=1, verbose_name='Вес')
    is_start_package = models.BooleanField(default=False, verbose_name='Начальный тариф')
    max_webinars = models.SmallIntegerField(default=0, verbose_name='Максимальное количество вебинаров')
    max_lending_to_webinar = models.SmallIntegerField(default=0, verbose_name='Максимальное количество лендингов у вебинара')
    can_create_premium_template = models.BooleanField(default=False, verbose_name='Может создавать премиум шаблоны')

    class Meta:
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'
        ordering = ('weight',)

    def __str__(self):
        return self.title

    def get_max_webinars(self):
        if self.max_webinars < 0:
            return format_html('&#8734;')
        return self.max_webinars

    get_max_webinars.short_description = 'Кол. вебинаров'

    def get_max_lending_to_webinar(self):
        if self.max_lending_to_webinar < 0:
            return format_html('&#8734;')
        return self.max_lending_to_webinar

    get_max_lending_to_webinar.short_description = 'Кол. лендигов у вебинара'

    def get_price(self):
        if self.price == 0:
            return 'Free'
        return '{} USD'.format(self.price)

    get_price.short_description = 'Цена'


