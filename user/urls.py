from django.urls import path

from user.views import UserLoginView, UserLogoutView

app_name = 'user'

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
