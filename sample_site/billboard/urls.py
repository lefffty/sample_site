from django.urls import path

from . import views

app_name = 'billboard'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'boards/<int:billboard_id>/',
        views.billboard_detail,
        name='billboard_detail',
    ),
    path(
        'boards/<slug:category_name>/',
        views.category_list,
        name='category_bbs',
    ),
    path(
        'board/create/',
        views.BillBoardCreateView.as_view(),
        name='create_billboard',
    )
]
