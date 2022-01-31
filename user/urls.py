from django.urls import path

from user.views import login, UserLogoutView

app_name = 'user'

urlpatterns = [
    path('', login, name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
