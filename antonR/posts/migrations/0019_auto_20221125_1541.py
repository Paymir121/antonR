# Generated by Django 2.2.16 on 2022-11-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_auto_20221125_1529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Картинка', 'verbose_name_plural': 'Картинки'},
        ),
        migrations.AddField(
            model_name='post',
            name='title_post',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
