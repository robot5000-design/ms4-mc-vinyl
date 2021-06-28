# Generated by Django 3.2.3 on 2021-06-27 20:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20210627_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.SlugField(validators=[django.core.validators.RegexValidator('^[-a-zA-Z0-9_]+$', 'invalid entries')]),
        ),
    ]
