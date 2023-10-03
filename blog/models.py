from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    view_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    published_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
