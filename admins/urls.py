from django.urls import path

from admins.views import UserCreateView, UserListView, UserAdminView, UserAdminDelete, UserAdminRehub

app_name = 'admins'

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
    path('users/', UserCreateView.as_view(), name='admins_users_create'),
    path('users_update/<int:pk>', UserAdminView.as_view(), name='admins_users_update'),
    path('users_delete/<int:pk>', UserAdminDelete.as_view(), name='admins_users_delete'),
    path('users_rehub/<int:pk>', UserAdminRehub.as_view(), name='admins_users_rehub'),

]
