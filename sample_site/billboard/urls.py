from django.urls import path

from . import views

app_name = 'billboard'

urlpatterns = [
    path(
        '',
        views.BillBoardListView.as_view(),
        name='index',
    ),
    path(
        'boards/<int:pk>/',
        views.BillBoardDetailView.as_view(),
        name='billboard_detail',
    ),
    path(
        'boards/<slug:category_name>/',
        views.CategoryListView.as_view(),
        name='category_bbs',
    ),
    path(
        'board/create/',
        views.BillBoardCreateView.as_view(),
        name='create_billboard',
    ),
    path(
        'board/<int:pk>/edit/',
        views.BillBoardUpdateView.as_view(),
        name='update_billboard',
    ),
    path(
        'board/<int:pk>/delete/',
        views.BillBoardDeleteView.as_view(),
        name='delete_billboard',
    ),
    path(
        'board/<int:pk>/comments/create',
        views.CommentCreate.as_view(),
        name='create_comment',
    ),
    path(
        'board/<int:pk>/comments/<int:comment_id>/',
        views.CommentUpdate.as_view(),
        name='update_comment',
    ),
    path(
        'board/<int:pk>/comments/<int:comment_id>/',
        views.CommentDelete.as_view(),
        name='delete_comment',
    )
]
