from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView

from user.forms import UserLoginForm
from user.models import User


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse('main:index', args=(self.request.user.id, ))


class UserLogoutView(LogoutView):
    next_page = '/'