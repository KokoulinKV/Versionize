from django.urls import path

from admins.views import UserCreateView, UserListView, UserEditView, UserDeleteView, UserRehubView, CompanyListView, \
    CompanyEditView, CompanyCreateView, CompanyAdminDelete, CompanyAdminDeleteMessage, UserAddInfoView, \
    UserInfoListView, UserInfoEdit, CreateStandartSections, StandartSectionsListView

app_name = 'admins'

urlpatterns = [
    # Users
    path('', UserListView.as_view(), name='index'),
    path('users/', UserCreateView.as_view(), name='admins_users_create'),
    path('users_update/<int:pk>', UserEditView.as_view(), name='admins_users_update'),
    path('users_delete/<int:pk>', UserDeleteView.as_view(), name='admins_users_delete'),
    path('users_rehub/<int:pk>', UserRehubView.as_view(), name='admins_users_rehub'),

    # User's Info
    path('users_info/', UserInfoListView.as_view(), name='admins_usersinfo'),
    path('users_addinfo/', UserAddInfoView.as_view(), name='admins_addinfo'),
    path('users_infoedit/<int:pk>', UserInfoEdit.as_view(), name='admins_usersinfo_edit'),

    # Companies
    path('companies/', CompanyListView.as_view(), name='admins_companies'),
    path('companies_update/<int:pk>', CompanyEditView.as_view(), name='admins_companies_update'),
    path('companies_create/', CompanyCreateView.as_view(), name='admins_companies_create'),
    path('companies_delete_message/<int:pk>', CompanyAdminDeleteMessage.as_view(),
         name='admins_companies_delete_message'),
    path('companies_delete/<int:pk>', CompanyAdminDelete.as_view(), name='admins_companies_delete'),

    # Standart Sections
    path('sections_create/', CreateStandartSections.as_view(), name='admins_sections_create'),
    path('sections/', StandartSectionsListView.as_view(), name='admins_sections'),
]
