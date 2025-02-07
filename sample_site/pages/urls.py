from .views import About, Rules
from django.urls import path


app_name = 'pages'

urlpatterns = [
    path('rules/', Rules.as_view(), name='rules'),
    path('about/', About.as_view(), name='about'),
]
