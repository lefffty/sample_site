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
]
