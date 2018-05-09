# Generated by Django 2.0.2 on 2018-04-03 09:18

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mlm_builder.utils
import phonenumber_field.modelfields
import profile_mlm.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('package', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('avatar', sorl.thumbnail.fields.ImageField(blank=True, default=None, null=True, upload_to=mlm_builder.utils.set_filename, verbose_name='Аватар')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Обо мне')),
                ('is_push_email', models.BooleanField(default=True, verbose_name='Получать Email уведомления')),
                ('website', models.URLField(blank=True, verbose_name='Сайт')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=30, verbose_name='Телефон')),
                ('skype', models.CharField(blank=True, max_length=150, verbose_name='Логин в Skype')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Баланс')),
                ('link_vkontakte', models.URLField(blank=True, verbose_name='Ссылка на страницу ВКонтакте')),
                ('link_facebook', models.URLField(blank=True, verbose_name='Ссылка на страницу Facebook')),
                ('link_twitter', models.URLField(blank=True, verbose_name='Ссылка на страницу Twitter')),
                ('link_instagram', models.URLField(blank=True, verbose_name='Ссылка на страницу Instagram')),
                ('link_odnoklassniki', models.URLField(blank=True, verbose_name='Ссылка на страницу Одноклассники')),
                ('link_my_world', models.URLField(blank=True, verbose_name='Ссылка на страницу Мой мир')),
                ('package_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания тарифа')),
                ('package', models.ForeignKey(blank=True, default=profile_mlm.models.set_default_package, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='package.Package', verbose_name='Тарифный план')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
    ]
