# Generated by Django 2.2.16 on 2022-11-23 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20221123_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='like',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]