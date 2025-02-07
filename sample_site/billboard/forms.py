from django import forms

from .models import BillBoard, Comment


class BillBoardForm(forms.ModelForm):
    class Meta:
        model = BillBoard
        fields = ('title', 'content', 'price', 'category', 'kind',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
