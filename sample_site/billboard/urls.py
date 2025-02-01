from django.urls import path

from . import views

app_name = 'billboard'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'boards/<slug:category_name>/',
        views.category_list,
        name='category_bbs',
    ),
    path(
        'category/<int:billboard_id>/',
        views.billboard_detail,
        name='billboard_detail',
    ),
    path(
        'category/create/',
        views.BillBoardCreateView.as_view(),
        name='create_billboard',
    )
]
