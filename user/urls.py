from django.urls import path

from user.views import login, logout

app_name = 'user'

urlpatterns = [
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
]
