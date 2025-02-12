from django import forms
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

from .models import (
    BillBoard,
    Comment,
    Category,
)


User = get_user_model()


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
        fields = ('title', 'content', 'price', 'image', 'category', 'kind',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class BillBoardSearchForm(forms.Form):
    field_order = ('')
    billboard_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория товара',
    )
    billboard_kind = forms.ChoiceField(
        choices=BillBoard.Kinds.choices,
        label='Тип сделки',
    )
    price_min = forms.FloatField(
        label='Мин. цена',
    )
    price_max = forms.FloatField(
        label='Макс. цена',
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
