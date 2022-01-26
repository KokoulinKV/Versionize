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

@register.inclusion_tag('main/lk.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(to_user=request.user.id).exclude(user_has_seen=True).order_by('-date')
    return {'notifications': notifications}