from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(blank=True, verbose_name='контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', max_length=200, blank=True, verbose_name='изображение')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='категория')
    views = models.IntegerField(default=0, verbose_name='количество просмотров')

    # Работает аналогично тегу { url 'name_of_url_address' }
    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='название категории')

    # Работает аналогично тегу { url 'name_of_url_address' }
    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['title']
