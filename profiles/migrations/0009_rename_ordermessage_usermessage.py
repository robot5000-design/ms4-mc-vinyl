# Generated by Django 3.2.3 on 2021-06-28 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20210628_1559'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderMessage',
            new_name='UserMessage',
        ),
    ]
