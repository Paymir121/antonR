# Generated by Django 2.2.16 on 2022-11-27 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_auto_20221125_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_post', to='posts.Post', verbose_name='Картинка К Посту'),
        ),
    ]
