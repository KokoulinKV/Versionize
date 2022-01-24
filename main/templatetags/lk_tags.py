from atexit import register
import imp
from django import template
from main.models import Project

register = template.Library()


@register.simple_tag(name='user-projects')
def get_user_project(filter=None):
    if not filter:
        return Project.objects.all()

    else:
        return Project.objects.filter(admin_id=filter)