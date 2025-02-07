from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


urlpatterns = [
    path('pages/', include('pages.urls')),
    path('', include('billboard.urls')),
    path('admin/', admin.site.urls),
    # path('auth/', include('django.contrib.auth.urls')),
    # path(
    #     'auth/registration/',
    #     CreateView.as_view(
    #         template_name='registration/registration.html',
    #         form_class=UserCreationForm,
    #         success_url=reverse_lazy('billboard:index'),
    #     ),
    #     name='registration',
    # )
]
