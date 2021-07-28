# Generated by Django 3.2.3 on 2021-07-27 13:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_alter_genre_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(regex='^[-a-z0-9_]+$')]),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(regex='^[-a-z0-9_]+$')]),
        ),
    ]