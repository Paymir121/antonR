# Generated by Django 2.2.6 on 2022-11-15 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20221114_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст коментария', verbose_name='Текст коментария')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор коментария')),
                ('post', models.ForeignKey(blank=True, help_text='комментарий к которой будет относиться пост', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='posts.Post', verbose_name='комментарий')),
            ],
        ),
    ]