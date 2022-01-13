from django.urls import path

from admins.views import UserCreateView, UserListView, UserAdminView, UserAdminDelete, UserAdminRehub, CompanyListView, \
    CompanyAdminView, CompanyCreateView, CompanyAdminDelete, CompanyAdminDeleteMessage

app_name = 'admins'

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
    path('users/', UserCreateView.as_view(), name='admins_users_create'),
    path('users_update/<int:pk>', UserAdminView.as_view(), name='admins_users_update'),
    path('users_delete/<int:pk>', UserAdminDelete.as_view(), name='admins_users_delete'),
    path('users_rehub/<int:pk>', UserAdminRehub.as_view(), name='admins_users_rehub'),

    path('companies/', CompanyListView.as_view(), name='admins_companies'),
    path('companies_update/<int:pk>', CompanyAdminView.as_view(), name='admins_companies_update'),
    path('companies_create/', CompanyCreateView.as_view(), name='admins_companies_create'),
    path('companies_delete_message/<int:pk>', CompanyAdminDeleteMessage.as_view(),
         name='admins_companies_delete_message'),
    path('companies_delete/<int:pk>', CompanyAdminDelete.as_view(), name='admins_companies_delete'),
]
