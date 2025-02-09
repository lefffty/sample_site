from django.urls import path

from .views import (
    api_categories,
    api_category_detail,
    api_billboards,
    api_billboard_detail,
    api_comments,
)


urlpatterns = [
    path(
        'v1/categories/',
        api_categories,
        name='api-categories'
    ),
    path(
        'v1/category/<int:pk>/',
        api_category_detail,
        name='api-category-detail'
    ),
    path(
        'v1/billboards/',
        api_billboards,
        name='api-billboards',
    ),
    path(
        'v1/billboard/<int:pk>/',
        api_billboard_detail,
        name='api-billboard-detail',
    ),
    path(
        'v1/comments/',
        api_comments,
        name='api-comments',
    )
]
