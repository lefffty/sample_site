from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)
from django.contrib.auth import get_user_model

from billboard.models import Category, BillBoard, Comment


User = get_user_model()


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug',)


class BillBoardSerializer(ModelSerializer):
    kind = SerializerMethodField()
    category = StringRelatedField(read_only=True)
    comments = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = BillBoard
        fields = ('title', 'category', 'content',
                  'price', 'kind', 'published_at', 'comments')

    def get_kind(self, obj):
        return obj.get_kind_display()


class CommentSerializer(ModelSerializer):
    billboard = StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('text', 'created_at', 'billboard')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
