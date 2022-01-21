from django.contrib import admin

# Register your models here.
from main.models import Project, Section, Document, Adjustment, Remark, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Project._meta.fields if field.name != "id"
    ]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Section._meta.fields if field.name != "id"
    ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Document._meta.fields if field.name != "id"
    ]


@admin.register(Adjustment)
class AdjustmentAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Adjustment._meta.fields if field.name != "id"
    ]


@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Remark._meta.fields if field.name != "id"
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Comment._meta.fields if field.name != "id"
    ]
