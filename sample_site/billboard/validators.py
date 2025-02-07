from django.core.exceptions import ValidationError


def validate_price(value):
    if value < 0:
        raise ValidationError(
            'Число %(value)s отрицательное',
            code='odd',
            params={
                'value': value,
            }
        )


def validate_title(title: str):
    if title.isdigit():
        raise ValidationError(
            'Название объявления не должно являться числом!',
            code='invalid',
        )
