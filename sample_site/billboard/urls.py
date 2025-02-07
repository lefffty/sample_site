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
    )
]
