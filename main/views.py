import os

from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from Versionize import settings

from main.forms import DocumentForm, AddSectionForm, CreateProjectForm, AddRemarkDocSectionForm, \
    AddRemarkDocProjectForm, PasswordChangeForm, PhotoForm, EmailPhoneEditForm, DocumentSectionForm, \
    PermissionCardForm, InfoCardForm

from main.func import download_some_files, download_single_file, _get_form, ajax_check, clear_form_data
from main.models import Section, Company, Document, Project, Comment, RemarksDocs
from main.utils.card_generation import generate_info_card, generate_permission_card


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'main/lk.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        doc_form = DocumentForm(prefix='doc_form_pre')
        if request.session['active_project_id']:
            if request.user.check_user():
                doc_form.fields['section'].queryset = \
                    Section.objects.filter(project_id=request.session['active_project_id'])
            else:
                doc_form.fields['section'].queryset = \
                    Section.objects.filter(project_id=request.session['active_project_id']) \
                        .filter(responsible_id=request.user.id)
        else:
            doc_form.fields['section'].queryset =''


        to_response = {'doc_form': doc_form,
             'add_section_form': AddSectionForm(prefix='add_section_form_pre'),
             'create_project_form': CreateProjectForm(prefix='create_project_form_pre'),
             'change_password_form': PasswordChangeForm(prefix='change_password_form_pre',
                                                         user=self.request.user),
             'photo_form':PhotoForm(prefix='photo_form_pre'),
             'email_form':EmailPhoneEditForm(instance=request.user, prefix='email_form_pre')}

        to_response.update(context)
        return self.render_to_response(to_response)

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        add_section_form = _get_form(request, AddSectionForm, 'add_section_form_pre')
        create_project_form = _get_form(request, CreateProjectForm, 'create_project_form_pre')
        change_password_form = _get_form(request, PasswordChangeForm, 'change_password_form_pre', user=self.request.user)
        photo_form = _get_form(request, PhotoForm, 'photo_form_pre')
        email_form = _get_form(request, EmailPhoneEditForm, 'email_form_pre')

        # @TheSleepyNomad
        # Выполняем проверку на ajax запрос
        if request.method == 'POST' and ajax_check(request):
            # В текущей версии разработки меняем только текущий активный проект
            # Todo написать алгоритм, по которому будем определять имя функции ajax
            # Пользователь выбирает наименование/код, но передаем id, так как наименование пока может повторяться
            project_id = request.POST.get('project_id', None)
            request.session['active_project_id'] = project_id
            response = {'status': True}
            return JsonResponse(response)

        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.instance.name = str(doc_form.instance.doc_path)
                doc_form.save()
                doc_form.data = clear_form_data(doc_form.data)
            except ValidationError:
                errors = 'Файл для загрузки не был выбран, формат выбранного файла не является' \
                         ' "pdf" или данная версия документа уже была загружена. Загрузите корректный файл.'
                # TODO Подумать как записывать ошибки нескольких форм
                return self.render_to_response({
                    'doc_form': doc_form,
                    'add_section_form': add_section_form,
                    'create_project_form': create_project_form,
                    'errors': errors
                })
        elif add_section_form.is_bound and add_section_form.is_valid():
            add_section_form.instance.project_id = request.session['active_project_id']
            add_section_form.save()
            add_section_form.data = clear_form_data(add_section_form.data)

        elif create_project_form.is_bound and create_project_form.is_valid():
            create_project_form.save()
            create_project_form.data = clear_form_data(create_project_form.data)

        elif change_password_form.is_bound and change_password_form.is_valid():
            change_password_form.save()
            update_session_auth_hash(self.request, change_password_form.user)
            change_password_form.data = clear_form_data(change_password_form.data)

        elif photo_form.is_bound and photo_form.is_valid():
            photo_form.instance = request.user
            photo_form.save()
            photo_form.data = clear_form_data(photo_form.data)

        elif email_form.is_bound and email_form.is_valid():
            email_form.instance = request.user
            email_form.save()

        return HttpResponseRedirect(reverse('main:index', args=(kwargs['pk'],)))


class TotalListView(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get_queryset(self):
        # Собираем модели Document, Section, Company, Project
        section_queryset = Section.objects.filter(
            project_id=self.request.session['active_project_id']
        ).values(
            'id', 'abbreviation', 'project', 'responsible_id', 'project__code', 'company__name',
            'document__id', 'document__md5', 'document__doc_path',
            'document__status', 'document__version',
            'document__variation', 'document__note'
        ).order_by(
            'id', 'document__version'
        )
        filtered_queryset = []
        for i in range(len(section_queryset)):
            this_object = section_queryset[i]
            try:
                next_object = section_queryset[i + 1]
                # На случай, если в разделе отсутствуют документы
                if next_object['document__version'] is None:
                    filtered_queryset.append(this_object)
                    continue
                if this_object['document__version'] > next_object['document__version']:
                    filtered_queryset.append(this_object)
            except IndexError:
                filtered_queryset.append(this_object)
                return filtered_queryset
        # Возвращаем список объектов Document являющихся последними версиями в разделе
        return filtered_queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO оптимизировать запрос.
        #  Контекстный процессор пробрасывает объект Project на кажду страницу
        admin_data = Project.objects.get(id=self.request.session['active_project_id']).get_admin_data()
        context['admin_data'] = admin_data
        context['title'] = 'Сводная таблица проекта'
        return context

    def get(self, request, *args, **kwargs):
        doc_form = DocumentForm(prefix='doc_form_pre')
        if  request.user.check_user():
            doc_form.fields['section'].queryset = \
                Section.objects.filter(project_id=request.session['active_project_id'])
        else:
            doc_form.fields['section'].queryset = \
                Section.objects.filter(project_id=request.session['active_project_id'])\
                    .filter(responsible_id=request.user.id)
        context = self.get_context_data(**kwargs)

        actualremark = RemarksDocs.objects.filter(to_project=request.session['active_project_id'])
        if actualremark:
            actualremark = actualremark.latest('created_at')

        to_response = {'doc_form': doc_form,
                       'add_section_form': AddSectionForm(prefix='add_section_form_pre'),
                       'remarkdoc_form': AddRemarkDocProjectForm(prefix='remarkdoc_form_pre'),
                       'object_list': self.get_queryset(),
                       'actualremark': actualremark
                       }
        to_response.update(context)
        return self.render_to_response(to_response)

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        add_section_form = _get_form(request, AddSectionForm, 'add_section_form_pre')
        remarkdoc_form = _get_form(request, AddRemarkDocProjectForm, 'remarkdoc_form_pre')

        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.instance.name = str(doc_form.instance.doc_path)
                doc_form.save()
                doc_form.data = clear_form_data(doc_form.data)
            except ValidationError:
                errors = 'Файл для загрузки не был выбран, формат выбранного файла не является' \
                         ' "pdf" или данная версия документа уже была загружена. Загрузите корректный файл.'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'add_section_form': add_section_form,
                    'remarkdoc_form': remarkdoc_form,
                    'object_list': self.get_queryset(),
                    'errors': errors
                })
        elif add_section_form.is_bound and add_section_form.is_valid():
            add_section_form.instance.project_id = request.session['active_project_id']
            add_section_form.save()
            add_section_form.data = clear_form_data(add_section_form.data)

        elif remarkdoc_form.is_bound and remarkdoc_form.is_valid():
            remarkdoc_form.instance.to_project_id = request.session['active_project_id']
            remarkdoc_form.save()
            remarkdoc_form.data = clear_form_data(remarkdoc_form.data)
        return HttpResponseRedirect(reverse('main:total'))


class SectionDetailView(LoginRequiredMixin, DetailView):
    model = Section
    template_name = 'main/section.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        actualremark = RemarksDocs.objects.filter(to_section=kwargs['pk'])
        if actualremark:
            actualremark = actualremark.latest('created_at')

        to_response = {'doc_form': DocumentSectionForm(prefix='doc_form_pre'),
                       'remarkdoc_form': AddRemarkDocSectionForm(prefix='remarkdoc_form_pre'),
                       'section': self.get_object(),
                       'actualremark': actualremark}
        to_response.update(context)
        return self.render_to_response(to_response)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Раздел'
        return context

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentSectionForm, 'doc_form_pre')
        remarkdoc_form = _get_form(request, AddRemarkDocSectionForm, 'remarkdoc_form_pre')
        section = str(kwargs['pk'])
        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.instance.name = str(doc_form.instance.doc_path)
                doc_form.instance.section_id = kwargs['pk']
                doc_form.save()
                doc_form.data = clear_form_data(doc_form.data)
                return HttpResponseRedirect(reverse('main:section', args=(section)))
            except ValidationError:
                errors = 'Файл для загрузки не был выбран, формат выбранного файла не является' \
                         ' "pdf" или данная версия документа уже была загружена. Загрузите корректный файл.'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'remarkdoc_form': remarkdoc_form,
                    'section': self.get_object(),
                    'errors': errors
                })
        elif remarkdoc_form.is_bound and remarkdoc_form.is_valid():
            remarkdoc_form.instance.to_section_id = kwargs['pk']
            remarkdoc_form.save()
            remarkdoc_form.data = clear_form_data(remarkdoc_form.data)
            return HttpResponseRedirect(reverse('main:section', args=(section)))


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'main/companies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Компании'
        return context


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = 'main/document.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Документ'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        to_response = {'permission_card_form': PermissionCardForm(prefix='permission_card_pre'),
                       'info_card_form': InfoCardForm(prefix='info_card_pre')}
        to_response.update(context)
        return self.render_to_response(to_response)

    def post(self, request, *args, **kwargs):
        # @TheSleepyNomad
        # Выполняем проверку на ajax запрос
        if request.method == 'POST' and ajax_check(request):
            new_comment = Comment(
                author_id=request.user.id,
                document_id=self.kwargs['pk'],
                body=request.POST.get('commentBody'),)
            new_comment.save()
            to_response = {'status': True}
            return JsonResponse(to_response)

        permission_card_form = _get_form(request, PermissionCardForm, 'permission_card_pre')
        info_card_form = _get_form(request, InfoCardForm, 'info_card_pre')

        if permission_card_form.is_bound and permission_card_form.is_valid():
            form_prefix = 'permission_card_pre-'

            # Формируем словарь для функции
            data = {
                'document_id': self.kwargs['pk'],
                'permission_number': permission_card_form.data.get(f'{form_prefix}permission_number'),
                'norm_control': permission_card_form.data.get(f'{form_prefix}norm_control'),
                'changes_by': permission_card_form.data.get(f'{form_prefix}changes_by'),
                'made_by': permission_card_form.data.get(f'{form_prefix}made_by'),
                'approved_by': permission_card_form.data.get(f'{form_prefix}approved_by'),
            }
            # generate_permission_card формирует Разрешение и возвращает путь к нему
            card_path = generate_permission_card(data)
            # чистим форму
            permission_card_form.data = clear_form_data(permission_card_form.data)
            # download_single_file формирует архив с файлом и возвращает response
            return download_single_file(card_path)

        elif info_card_form.is_bound and info_card_form.is_valid():
            form_prefix = 'info_card_pre-'

            # Формируем словарь для функции
            data = {
                'document_id': self.kwargs['pk'],
                'developed_by': info_card_form.data.get(f'{form_prefix}developed_by'),
                'checked_by': info_card_form.data.get(f'{form_prefix}checked_by'),
                'norm_control': info_card_form.data.get(f'{form_prefix}norm_control'),
                'approved_by': info_card_form.data.get(f'{form_prefix}approved_by'),
                'manager_position': info_card_form.data.get(f'{form_prefix}manager_position'),
                'manager_name': info_card_form.data.get(f'{form_prefix}manager_name'),
            }
            # generate_permission_card формирует Разрешение и возвращает путь к нему
            card_path = generate_info_card(data)
            # чистим форму
            info_card_form.data = clear_form_data(info_card_form.data)
            # download_single_file формирует архив с файлом и возвращает response
            return download_single_file(card_path)

        return self.render_to_response({'permission_card_form': permission_card_form,
                                        'info_card_form': info_card_form})


class DocumentDownload(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        path = Document.objects.filter(id=context['pk']).values('doc_path')[0]['doc_path']
        return download_single_file(path)


class DocumentDownloadAllOfTotal(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        project = Project.objects.filter(id=context['pk'])[0]
        sections = Section.objects.filter(project_id=context['pk'])
        files_download = []
        for section in sections:
            if  Document.objects.filter(section=section):
                document = Document.objects.filter(section=section).values('doc_path').latest('created_at')['doc_path']
                dir, document = document.split('/')
                files_download.append(document)

        document_dir = os.path.join(settings.MEDIA_ROOT, dir)
        project_name = str(project).replace("/",'_')
        zip_name = f'{project_name}_docs.zip'

        return download_some_files(zip_name, document_dir, files_download)


class DocumentDownloadAllOfSection(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        section = Section.objects.filter(id=context['pk']).values('name')[0]['name']
        documents = Document.objects.filter(section_id=context['pk']).values('doc_path')
        files_download = []
        for document in documents:
            document = document['doc_path']
            dir, document = document.split('/')
            files_download.append(document)

        document_dir = os.path.join(settings.MEDIA_ROOT, dir)
        zip_name = f'{section}_docs.zip'

        return download_some_files(zip_name, document_dir, files_download)


class RemarkDocDownload(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        path = RemarksDocs.objects.filter(id=context['pk']).values('doc_path')[0]['doc_path']
        return download_single_file(path)


# @TheSleepyNomad
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'main/project.html'
    context_object_name = 'project'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проект'
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'main/projects.html'
    context_object_name = 'projects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проекты'
        return context
