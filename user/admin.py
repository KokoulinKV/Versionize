from django.contrib import admin

from user.models import User, Company, UserCompanyInfo

admin.site.register(User)
admin.site.register(Company)
admin.site.register(UserCompanyInfo)
