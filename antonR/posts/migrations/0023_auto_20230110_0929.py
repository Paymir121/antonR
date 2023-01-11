# Generated by Django 2.2.16 on 2023-01-10 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_auto_20221221_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='text',
            field=models.TextField(default=1, help_text='текст под картинкой', verbose_name='Описание картинки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, help_text='Тип проекта', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.Group', verbose_name='Тип проекта'),
        ),
    ]