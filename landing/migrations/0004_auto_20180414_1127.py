# Generated by Django 2.0.2 on 2018-04-14 11:27

from django.db import migrations, models
import landing.models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_remove_landing_landing_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='landing',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=landing.models.set_image_name, verbose_name='Изображение'),
        ),
    ]
