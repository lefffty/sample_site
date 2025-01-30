from django.db import models


class BillBoard(models.Model):
    title = models.CharField(max_length=50, verbose_name='Объявление')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    published_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано'
    )

    def __str__(self):
        return f'Объявление под названием {self.title}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published_at']
