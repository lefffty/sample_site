from django import forms

from .models import BillBoard


class BillBoardForm(forms.ModelForm):
    class Meta:
        model = BillBoard
        fields = ('title', 'content', 'price', 'category', 'kind',)
