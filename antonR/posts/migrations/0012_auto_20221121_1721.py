# Generated by Django 2.2.16 on 2022-11-21 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20221121_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PostLike', to='posts.Post', verbose_name='Лайк Посту'),
        ),
    ]