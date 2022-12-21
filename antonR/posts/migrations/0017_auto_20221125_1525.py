# Generated by Django 2.2.16 on 2022-11-25 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20221124_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Картинка')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_post', to='posts.Post', verbose_name='Лайк Посту')),
            ],
            options={
                'verbose_name': 'Лайки',
                'verbose_name_plural': 'Лайки',
                'unique_together': {('post', 'image')},
            },
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
