from django.db import models


class Category(models.Model):
    name = models.SlugField(unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class BillBoard(models.Model):
    title = models.CharField(max_length=50, verbose_name='Объявление')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    published_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Категория',
    )

    def __str__(self):
        return f'Объявление под названием {self.title}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['category__name', '-published_at']
