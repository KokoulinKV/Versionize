from atexit import register
import imp
from urllib import request
from django import template
from main.models import Project
from service.models import Notification

register = template.Library()


@register.simple_tag(name='user-projects')
def get_user_project(filter=None):
    if not filter:
        return Project.objects.all()

    else:
        return Project.objects.filter(admin_id=filter)

@register.simple_tag(name='notifications')
def get_user_notifications(filter=None):
    if not filter:
        return Notification.objects.all()

    else:
        return Notification.objects.filter(to_user=filter).exclude(user_has_seen=True).order_by('-data')