from django import forms
from captcha.fields import CaptchaField

from .models import (
    BillBoard,
    Comment,
    Category,
)


class BillBoardForm(forms.ModelForm):
    captcha = CaptchaField(
        label='Введите текст с картинки',
        error_messages={
            'invalid': 'Неправильный текст',
        },
        generator='captcha.helpers.random_char_challenge',
    )

    class Meta:
        model = BillBoard
        fields = ('title', 'content', 'price', 'category', 'kind',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class BillBoardSearchForm(forms.Form):
    field_order = ('')
    billboard_kind = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория товара',
    )
    price_min = forms.FloatField()
    price_max = forms.FloatField()
