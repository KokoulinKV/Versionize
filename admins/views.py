from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView

from admins.forms import UserRegistrationForm, CompanyRegistrationFrom, CompanyEditForm, \
    UserCompanyInfoForm, UserAddInfoForm

from user.models import User, Company, UserCompanyInfo

'''
    Views for main user data: list, create, edit, delete and rehub
    Main user data: username, firstname, lastname, patronymic, image, email, phone, password
'''


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


class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('admins:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserEditView(UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('admins:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        context['title'] = 'Edit user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserEditView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'
    form_class = UserCompanyInfoForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('admins:index'))


class UserRehubView(UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'
    form_class = UserCompanyInfoForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserRehubView, self).get_context_data(**kwargs)
        context['title'] = 'Rehub user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('admins:index'))


'''
    Views for data about user's companies: list, create, edit, delete and rehub
    Main user data: username, firstname, lastname, patronymic, image, email, phone, password
'''


class UserInfoListView(ListView):
    model = UserCompanyInfo
    template_name = 'admins/admin-usersinfo.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserInfoListView, self).get_context_data(**kwargs)
        context['title'] = 'Users info'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserInfoListView, self).dispatch(request, *args, **kwargs)


class UserAddInfoView(CreateView):
    model = UserCompanyInfo
    template_name = 'admins/admin-users-addinfo.html'
    form_class = UserAddInfoForm
    success_url = reverse_lazy('admins:admins_usersinfo')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserAddInfoView, self).get_context_data(**kwargs)
        context['title'] = 'Add information about user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserAddInfoView, self).dispatch(request, *args, **kwargs)


class UserInfoEdit(UpdateView):
    model = UserCompanyInfo
    template_name = 'admins/admin-usersinfo-edit.html'
    form_class = UserCompanyInfoForm
    success_url = reverse_lazy('admins:admins_usersinfo')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserInfoEdit, self).get_context_data(**kwargs)
        context['title'] = 'Edit user'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserInfoEdit, self).dispatch(request, *args, **kwargs)


'''
    Views for companies: list, create, edit, delete message and delete 
'''


class CompanyListView(ListView):
    model = Company
    template_name = 'admins/admin-companies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)
        context['title'] = 'Companies'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyListView, self).dispatch(request, *args, **kwargs)


class CompanyCreateView(CreateView):
    model = Company
    template_name = 'admins/admin-companies-create.html'
    form_class = CompanyRegistrationFrom
    success_url = reverse_lazy('admins:admins_companies')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create company'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyCreateView, self).dispatch(request, *args, **kwargs)


class CompanyEditView(UpdateView):
    model = Company
    template_name = 'admins/admin-companies-edit.html'
    form_class = CompanyEditForm
    success_url = reverse_lazy('admins:admins_companies')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyEditView, self).get_context_data(**kwargs)
        context['title'] = 'Edit company'
        print(context)
        return context

    def form_valid(self, form):
        formset = form.save()
        user = formset.manager
        company = formset.id
        query = UserCompanyInfo.objects.select_related().filter(user_id=user)
        query.update(company=company)
        self.object = form.save()
        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyEditView, self).dispatch(request, *args, **kwargs)


class CompanyAdminDeleteMessage(UpdateView):
    model = Company
    template_name = 'admins/admin-companies-message.html'
    form_class = CompanyRegistrationFrom
    success_url = reverse_lazy('admins:admins_companies')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyAdminDeleteMessage, self).get_context_data(**kwargs)
        context['title'] = 'Message'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CompanyAdminDeleteMessage, self).dispatch(request, *args, **kwargs)


class CompanyAdminDelete(UpdateView):
    model = Company
    template_name = 'admins/admin-companies-message.html'
    form_class = CompanyRegistrationFrom

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyAdminDelete, self).get_context_data(**kwargs)
        context['title'] = 'Users'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(reverse_lazy('admins:admins_companies'))
