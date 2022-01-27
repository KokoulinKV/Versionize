from django.urls import path

from admins.views import UserCreateView, UserListView, UserEditView, UserDeleteView, UserRehubView, CompanyListView, \
    CompanyEditView, CompanyCreateView, CompanyAdminDelete, CompanyAdminDeleteMessage, \
    UserInfoListView, UserInfoEdit, CreateStandartSections, StandartSectionsListView, StandartSectionsEditView, \
    StandartSectionsDeleteMessage, StandartSectionsDelete

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
    path('sections_update/<int:pk>', StandartSectionsEditView.as_view(), name='admins_sections_update'),
    path('sections_delete_message/<int:pk>', StandartSectionsDeleteMessage.as_view(),
         name='admins_standartsections_delete_message'),
    path('sections_delete/<int:pk>', StandartSectionsDelete.as_view(), name='admins_sections_delete'),

]
