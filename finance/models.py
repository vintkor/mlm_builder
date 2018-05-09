from django.db import models
from mlm_builder.basemodel import BaseModel
from django.core.validators import validate_slug


# TODO Переопределить save - если ставим главную валюту True, остальные не False
class Currency(BaseModel):
    title = models.CharField(verbose_name='Заголовок', max_length=100, unique=True)
    code = models.CharField(verbose_name='ISO Code', max_length=3, unique=True, validators=[validate_slug])
    course = models.DecimalField(verbose_name='Курс по отношению к главной валюте', max_digits=10, decimal_places=4)
    is_main = models.BooleanField(default=False, verbose_name='Главная')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.code

    def save(self, **kwargs):
        self.code = self.code.upper()
        super(Currency, self).save(kwargs)

