from django.contrib import admin

# Register your models here.
from main.models import Project, Section, Document, Adjustment, Remark, Comment

admin.site.register(Project)
admin.site.register(Section)
admin.site.register(Document)
admin.site.register(Adjustment)
admin.site.register(Remark)
admin.site.register(Comment)