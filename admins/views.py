from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from admins.forms import UserRegistrationForm, CompanyRegistrationFrom, CompanyEditForm, \
    UserCompanyInfoForm, StandardSectionCreateForm, UserEditForm, UserChangePasswordForm
from main.models import StandardSection

from user.models import User, Company, UserCompanyInfo


# View for protect admins from not superusers
class AdminsLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


'''
    Views for main user data: list, create, edit, delete and rehub
    Main user data: username, firstname, lastname, patronymic, image, email, phone, password
'''


class UserListView(AdminsLoginRequiredMixin, ListView):
    model = User
    template_name = 'admins/admin-users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Учетные записи пользователей'
        return context


class UserCreateView(AdminsLoginRequiredMixin, CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('admins:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавление учетной записи пользователя'
        return context


class UserEditView(AdminsLoginRequiredMixin, UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'
    form_class = UserEditForm
    success_url = reverse_lazy('admins:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        context['title'] = f'Редактирование учетной записи пользователя {context["user"]}'
        return context


class UserChangePasswordView(AdminsLoginRequiredMixin, UpdateView):
    model = User
    template_name = 'admins/admin-users-change-password.html'
    form_class = UserChangePasswordForm
    success_url = reverse_lazy('admins:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserChangePasswordView, self).get_context_data(**kwargs)
        context['title'] = f'Смена пароля учетной записи пользователя {context["user"]}'
        return context

    def form_valid(self, form):
        self.object = form.save()
        update_session_auth_hash(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class UserDeleteView(AdminsLoginRequiredMixin, UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('admins:index'))


class UserRehubView(AdminsLoginRequiredMixin, UpdateView):
    model = User
    template_name = 'admins/admin-users-edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('admins:index'))


'''
    Views for data about user's companies: list, edit, delete and rehub
    Main user data: username, firstname, lastname, patronymic, image, email, phone, password
'''


class UserInfoListView(AdminsLoginRequiredMixin, ListView):
    template_name = 'admins/admin-usersinfo.html'
    queryset = UserCompanyInfo.objects.all().select_related('user', 'company')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserInfoListView, self).get_context_data(**kwargs)
        context['title'] = 'Информация о пользователях'
        return context


class UserInfoEdit(AdminsLoginRequiredMixin, UpdateView):
    model = UserCompanyInfo
    template_name = 'admins/admin-usersinfo-edit.html'
    form_class = UserCompanyInfoForm
    success_url = reverse_lazy('admins:admins_usersinfo')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserInfoEdit, self).get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя {context["usercompanyinfo"].user}'
        return context

    def form_valid(self, form):
        formset = form.save()
        user = formset.user_id
        company = formset.company_id
        check_manager = Company.objects.filter(manager_id=user).values('id')
        if check_manager:
            check_manager = check_manager[0]['id']
            if not (company == check_manager):
                manager_company_id = check_manager
                query = Company.objects.filter(id=manager_company_id)
                query.update(manager=None)
        return super().form_valid(form)


'''
    Views for companies: list, create, edit, delete message and delete 
'''


class CompanyListView(AdminsLoginRequiredMixin, ListView):
    model = Company
    template_name = 'admins/admin-companies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)
        context['title'] = 'Компании'
        return context


class CompanyCreateView(AdminsLoginRequiredMixin, CreateView):
    model = Company
    template_name = 'admins/admin-companies-create.html'
    form_class = CompanyRegistrationFrom
    success_url = reverse_lazy('admins:admins_companies')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавление компании'
        return context

    def form_valid(self, form):
        formset = form.save()
        user = formset.manager
        company = formset.id
        query = UserCompanyInfo.objects.select_related().filter(user_id=user)
        query.update(company=company)
        return super().form_valid(form)


class CompanyEditView(AdminsLoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'admins/admin-companies-edit.html'
    form_class = CompanyEditForm
    success_url = reverse_lazy('admins:admins_companies')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyEditView, self).get_context_data(**kwargs)
        context['title'] = f'Редактирование данных о компании {context["company"]}'
        return context

    def form_valid(self, form):
        formset = form.save()
        user = formset.manager
        company = formset.id
        query = UserCompanyInfo.objects.select_related().filter(user_id=user)
        query.update(company=company)
        return super().form_valid(form)


class CompanyAdminDeleteMessage(AdminsLoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'admins/admin-companies-message.html'
    form_class = CompanyRegistrationFrom
    success_url = reverse_lazy('admins:admins_companies')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyAdminDeleteMessage, self).get_context_data(**kwargs)
        context['title'] = f'Подтверждение удаления компании {context["company"]}'
        return context


class CompanyAdminDelete(AdminsLoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'admins/admin-companies-message.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(reverse_lazy('admins:admins_companies'))


'''
    Views for standartsections:  list, create, edit, delete message and delete 
'''


class CreateStandartSections(AdminsLoginRequiredMixin, CreateView):
    model = StandardSection
    template_name = 'admins/admin-standartsection-create.html'
    form_class = StandardSectionCreateForm
    success_url = reverse_lazy('admins:admins_sections')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CreateStandartSections, self).get_context_data(**kwargs)
        context['title'] = 'Добавлени стандартного раздела проекта'
        return context


class StandartSectionsListView(AdminsLoginRequiredMixin, ListView):
    model = StandardSection
    template_name = 'admins/admin-standartsections.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StandartSectionsListView, self).get_context_data(**kwargs)
        context['title'] = 'Стандартные разделы'
        return context


class StandartSectionsEditView(AdminsLoginRequiredMixin, UpdateView):
    model = StandardSection
    template_name = 'admins/admin-standartsections-edit.html'
    form_class = StandardSectionCreateForm
    success_url = reverse_lazy('admins:admins_sections')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StandartSectionsEditView, self).get_context_data(**kwargs)
        context['title'] = f'Редактирование стандартного раздела {context["standardsection"]}'
        return context


class StandartSectionsDeleteMessage(AdminsLoginRequiredMixin, UpdateView):
    model = StandardSection
    template_name = 'admins/admin-sections-message.html'
    form_class = StandardSectionCreateForm
    success_url = reverse_lazy('admins:admins_sections')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StandartSectionsDeleteMessage, self).get_context_data(**kwargs)
        context['title'] = f'Подтверждение удаления раздела {context["standardsection"]}'
        return context


class StandartSectionsDelete(AdminsLoginRequiredMixin, UpdateView):
    model = StandardSection
    template_name = 'admins/admin-sections-message.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(reverse_lazy('admins:admins_sections'))
