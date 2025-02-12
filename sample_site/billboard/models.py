from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
import uuid

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


class Purchase(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Покупатель',
        related_name='buyer',
    )
    item_name = models.CharField(
        max_length=50,
        verbose_name='Объявление',
    )
    salesman = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Продавец',
        related_name='salesman',
    )
    cost = models.FloatField(
        verbose_name='Цена',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Сделка оформлена',
    )


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
    unique_bb_id = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False,
    )
    content = models.TextField(
        verbose_name='Описание',
        blank=False,
    )
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
        default=Kinds.__empty__,
        verbose_name='Тип сделки',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор объявления',
    )
    image = models.ImageField(
        blank=True,
        default='images/billboard.jpg',
        verbose_name='Изображение',
        upload_to='images/%Y/%m/%d/',
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=('jpg', 'png', 'jpeg',)
            )
        ],
        error_messages={
            'invalid_extension': 'Этот формат не поддерживается'
        }
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['category__slug', '-published_at']


class Comment(models.Model):
    billboard = models.ForeignKey(
        BillBoard,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        blank=False,
        verbose_name='Текст комментария',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Автор комментария',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.text}'
