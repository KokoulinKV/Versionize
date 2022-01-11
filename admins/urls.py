from django.urls import path

from admins.views import UserCreateView, UserListView, UserAdminView

app_name = 'admins'

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
    path('users/', UserCreateView.as_view(), name='admins_users_create'),
    path('users/<int:pk>', UserAdminView.as_view(), name='admins_users_update'),
]
