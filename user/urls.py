from django.urls import path

from user.views import login #, lk

app_name = 'user'

urlpatterns = [
    path('', login, name='login'),
    # path('lk/', lk, name='lk'),
    # path('logout/', logout, name='logout'),
]
