from django.contrib import admin

from user.models import User, Company, UserCompanyInfo


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in User._meta.fields if field.name != "id"
    ]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Company._meta.fields if field.name != "id"
    ]


@admin.register(UserCompanyInfo)
class UserCompanyInfoAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in UserCompanyInfo._meta.fields
        if field.name != "id"
    ]