from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)
from billboard.models import Category, BillBoard


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug',)


class BillBoardSerializer(ModelSerializer):
    kind = SerializerMethodField()
    category = StringRelatedField(read_only=True)

    class Meta:
        model = BillBoard
        fields = ('id', 'title', 'category', 'content',
                  'price', 'kind', 'published_at')

    def get_kind(self, obj):
        return obj.get_kind_display()
