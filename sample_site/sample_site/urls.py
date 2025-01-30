from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('board/', include('billboard.urls')),
    path('admin/', admin.site.urls),
]
