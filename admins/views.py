from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView

from admins.forms import UserRegistrationFrom
from user.models import User, Company


class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserRegistrationFrom
    success_url = reverse_lazy('admins:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Users'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserAdminView(UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'
    form_class = UserRegistrationFrom
    success_url = reverse_lazy('admins:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserAdminView, self).get_context_data(**kwargs)
        context['title'] = 'Edit user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserAdminView, self).dispatch(request, *args, **kwargs)


class UserAdminDelete(UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'
    form_class = UserRegistrationFrom

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserAdminDelete, self).get_context_data(**kwargs)
        context['title'] = 'Users'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('admins:index'))


class UserAdminRehub(UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'
    form_class = UserRegistrationFrom

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserAdminRehub, self).get_context_data(**kwargs)
        context['title'] = 'Edit user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('admins:index'))
