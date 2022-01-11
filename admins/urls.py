from django.urls import path

from admins.views import admins_users_create, index

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', admins_users_create, name='admins_users_create'),
]
