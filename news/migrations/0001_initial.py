# Generated by Django 3.1 on 2020-08-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('content', models.TextField(blank=True, verbose_name='содержание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='изображение')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликовано')),
            ],
        ),
    ]
