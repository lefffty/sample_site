from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_price, validate_title


User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name='Идентификатор',
    )
    description = models.TextField(
        verbose_name='Описание категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['slug']

    def __str__(self):
        return self.title


class BillBoard(models.Model):
    class Kinds(models.IntegerChoices):
        BUY = 1, 'Покупка'
        SELL = 2, 'Продажа'
        EXCHANGE = 3, 'Обмен'
        RENT = 4, 'Аренда'
        __empty__ = 'Выберите тип публикуемого объявления'

    title = models.CharField(
        max_length=50,
        verbose_name='Объявление',
        validators=[validate_title],
    )
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(
        verbose_name='Цена',
        validators=[validate_price],
    )
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
    kind = models.SmallIntegerField(
        choices=Kinds.choices,
        default=Kinds.__empty__
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор объявления',
    )

    def __str__(self):
        return f'Объявление под названием {self.title}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['category__slug', '-published_at']
