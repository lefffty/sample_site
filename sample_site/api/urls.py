from django.urls import path

from . import views


urlpatterns = [
    path(
        'v1/categories/',
        views.api_categories,
        name='api-categories'
    ),
    path(
        'v1/category/<int:pk>/',
        views.api_category_detail,
        name='api-category-detail'
    ),
    path(
        'v1/billboards/',
        views.api_billboards,
        name='api-billboards',
    ),
    path(
        'v1/billboard/<int:pk>/',
        views.api_billboard_detail,
        name='api-billboard-detail',
    ),
    path(
        'v1/comments/',
        views.api_comments,
        name='api-comments',
    ),
    path(
        'v1/users/',
        views.api_users,
        name='api-users',
    ),
    path(
        'v1/user/<int:pk>/',
        views.api_user,
        name='api-user',
    )
]
