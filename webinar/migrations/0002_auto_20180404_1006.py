# Generated by Django 2.0.2 on 2018-04-04 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webinar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webinaruser',
            name='landing',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='landing.Landing', verbose_name='Ленгинг'),
        ),
    ]
