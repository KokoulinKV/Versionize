import os
import zipfile

from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from transliterate import translit
from django.http import JsonResponse

from Versionize import settings

from main.forms import DocumentForm, AddSectionForm, CreateProjectForm, \
    AddRemarkDocSectionForm, AddRemarkDocProjectForm, PermissionCardForm, InfoCardForm
from main.models import Section, Company, Document, Project, Comment, RemarksDocs
from main.utils.card_generation import generate_info_card

def ajax_check(request):
    # Проверяем отправлен ли нам post запрос через ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return True
    return False


def _get_form(request, formcls, prefix):
    if prefix in request.POST:
        data = request.POST
        if request.FILES:
            files = request.FILES
            return formcls(data, files, prefix=prefix)
    else:
        data = None
    return formcls(data, prefix=prefix)


def clear_form_data(form_data):
    """
    Clears the values of the immutable QueryDict instance
    """
    empty_dict = {'csrfmiddlewaretoken': form_data['csrfmiddlewaretoken']}
    for key in form_data.keys():
        empty_dict[form_data[key]] = ''
    return empty_dict


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'main/lk.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Сводная таблица проекта'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        to_response = {'doc_form': DocumentForm(prefix='doc_form_pre'),
             'add_section_form': AddSectionForm(prefix='add_section_form_pre'),
             'create_project_form': CreateProjectForm(prefix='create_project_form_pre')}
        to_response.update(context)
        return self.render_to_response(to_response)

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        add_section_form = _get_form(request, AddSectionForm, 'add_section_form_pre')
        create_project_form = _get_form(request, CreateProjectForm, 'create_project_form_pre')
        
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
                doc_form.save()
                doc_form.data = clear_form_data(doc_form.data)
            except ValidationError:
                errors = 'Данная версия документа уже была загружена. Загрузите корректную новую версию.'
                # TODO Подумать как записывать ошибки нескольких форм
                return self.render_to_response({
                    'doc_form': doc_form,
                    'add_section_form': add_section_form,
                    'create_project_form': create_project_form,
                    'errors': errors
                })
        elif add_section_form.is_bound and add_section_form.is_valid():
            add_section_form.save()
            add_section_form.data = clear_form_data(add_section_form.data)

        elif create_project_form.is_bound and create_project_form.is_valid():
            create_project_form.save()
            create_project_form.data = clear_form_data(create_project_form.data)
        return self.render_to_response({'doc_form': doc_form,
                                        'add_section_form': add_section_form,
                                        'create_project_form': create_project_form})


class TotalListView(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get_queryset(self):
        queryset = Section.objects.filter(
            project_id=self.request.session['active_project_id'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Сводная таблица проекта'
        return context

    def get(self, request, *args, **kwargs):
        remarkdoc_form = AddRemarkDocProjectForm(prefix='remarkdoc_form_pre')
        remarkdoc_form.fields['to_project'].queryset =\
            Project.objects.filter(id=request.session['active_project_id']).filter(
                id__in=Section.objects.filter(
                    id__in=Document.objects.all().values('section_id')
                ).values('project_id')
            )
        context = self.get_context_data(**kwargs)
        actualremark = RemarksDocs.objects.filter(to_project=
                                                      self.get_queryset().values('id')[0]['id'])
        if actualremark:
            actualremark = actualremark.latest('created_at')

        to_response = {'doc_form': DocumentForm(prefix='doc_form_pre'),
                       'add_section_form': AddSectionForm(prefix='add_section_form_pre'),
                       'remarkdoc_form': remarkdoc_form,
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
                doc_form.save()
                doc_form.data = clear_form_data(doc_form.data)
            except ValidationError:
                errors = 'Данная версия документа уже была загружена. Загрузите корректную новую версию.'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'add_section_form': add_section_form,
                    'remarkdoc_form': remarkdoc_form,
                    'object_list': self.get_queryset(),
                    'errors': errors
                })
        elif add_section_form.is_bound and add_section_form.is_valid():
            add_section_form.save()
            add_section_form.data = clear_form_data(add_section_form.data)

        elif remarkdoc_form.is_bound and remarkdoc_form.is_valid():
            remarkdoc_form.save()
            remarkdoc_form.data = clear_form_data(remarkdoc_form.data)
        return HttpResponseRedirect(reverse('main:total'))
        # return self.render_to_response({'doc_form': doc_form,
        #                                 'add_section_form': add_section_form,
        #                                 'remarkdoc_form': remarkdoc_form,
        #                                 'object_list': self.get_queryset()})


class SectionDetailView(LoginRequiredMixin, DetailView):
    model = Section
    template_name = 'main/section.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        doc_form = DocumentForm(prefix='doc_form_pre')
        doc_form.fields['section'].queryset = Section.objects.filter(id=kwargs['pk'])

        remarkdoc_form = AddRemarkDocSectionForm(prefix='remarkdoc_form_pre')
        remarkdoc_form.fields['to_section'].queryset = \
            Section.objects.filter(id=kwargs['pk']).filter(id__in=Document.objects.all().values('section_id'))

        actualremark = RemarksDocs.objects.filter(to_section=kwargs['pk'])
        if actualremark:
            actualremark = actualremark.latest('created_at')

        to_response = {'doc_form': doc_form,
                       'remarkdoc_form': remarkdoc_form,
                       'section': self.get_object(),
                       'actualremark': actualremark}
        to_response.update(context)
        return self.render_to_response(to_response)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Раздел'
        return context

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        remarkdoc_form = _get_form(request, AddRemarkDocSectionForm, 'remarkdoc_form_pre')
        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.save()
                section = doc_form.data['doc_form_pre-section']
                doc_form.data = clear_form_data(doc_form.data)
                return HttpResponseRedirect(reverse('main:section', args=(section)))
            except ValidationError:
                errors = 'Данная версия документа уже была загружена. Загрузите корректную новую версию.'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'remarkdoc_form': remarkdoc_form,
                    'section': self.get_object(),
                    'errors': errors
                })
        elif remarkdoc_form.is_bound and remarkdoc_form.is_valid():
            remarkdoc_form.save()
            section = remarkdoc_form.data['remarkdoc_form_pre-to_section']
            remarkdoc_form.data = clear_form_data(remarkdoc_form.data)
            return HttpResponseRedirect(reverse('main:section', args=(section)))
        # return self.render_to_response({'doc_form': doc_form,
        #                                 'remarkdoc_form': remarkdoc_form,
        #                                 'section': self.get_object()})


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'main/companies.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Компании'
        return context


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = 'main/document.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Документ'
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
            permission_card_form.data = clear_form_data(permission_card_form.data)

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
            generate_info_card(data)
        return self.render_to_response({'permission_card_form': permission_card_form,
                                        'info_card_form': info_card_form})


class DocumentDownload(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        path = Document.objects.filter(id=context['pk']).values('doc_path')[0]['doc_path']
        dir, document = path.split('/')
        document_dir = os.path.join(settings.MEDIA_ROOT, dir)
        translit_doc_name= translit(document, language_code='ru', reversed=True)
        zip_name = f'{translit_doc_name}.zip'
        zip_path = f'{settings.MEDIA_ROOT}/downloads/{zip_name}'
        archive = zipfile.ZipFile(zip_path, 'w')
        rootdir = os.path.basename(document_dir)

        for root, dir, files in os.walk(document_dir):
            for file in files:
                if file == document:
                    filepath = os.path.join(root, file)
                    parentpath = os.path.relpath(filepath, document_dir)
                    arcname = os.path.join(rootdir, parentpath)
                    archive.write(filepath, arcname)

        archive.close()


        if os.path.exists(zip_path):
            with open(zip_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream", )
                response['Content-Disposition'] = 'inline; filename=' + f'{zip_name}'
                return response
        raise Http404


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
        zip_name = f'{project}_docs.zip'
        translit_zip_name = translit(zip_name, language_code='ru', reversed=True)
        zip_path = f'{settings.MEDIA_ROOT}/downloads/{zip_name}'
        archive = zipfile.ZipFile(zip_path, 'w')
        rootdir = os.path.basename(document_dir)

        for root, dir, files in os.walk(document_dir):
            for file in files:
                if file in files_download:
                    filepath = os.path.join(root, file)
                    parentpath = os.path.relpath(filepath, document_dir)
                    arcname = os.path.join(rootdir, parentpath)
                    archive.write(filepath, arcname)
        archive.close()

        if os.path.exists(zip_path):
            with open(zip_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip", )
                response['Content-Disposition'] = 'inline; filename=' + f'{translit_zip_name}'
                return response
        raise Http404


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
        translit_zip_name = translit(zip_name, language_code='ru', reversed=True)
        zip_path = f'{settings.MEDIA_ROOT}/downloads/{zip_name}'
        archive = zipfile.ZipFile(zip_path, 'w')
        rootdir = os.path.basename(document_dir)

        for root, dir, files in os.walk(document_dir):
            for file in files:
                if file in files_download:
                    filepath = os.path.join(root, file)
                    parentpath = os.path.relpath(filepath, document_dir)
                    arcname = os.path.join(rootdir, parentpath)
                    archive.write(filepath, arcname)
        archive.close()

        if os.path.exists(zip_path):
            with open(zip_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip", )
                response['Content-Disposition'] = 'inline; filename=' + f'{translit_zip_name}'
                return response
        raise Http404


class RemarkDocDownload(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        path = RemarksDocs.objects.filter(id=context['pk']).values('doc_path')[0]['doc_path']
        dir, document = path.split('/')
        document_dir = os.path.join(settings.MEDIA_ROOT, dir)
        translit_doc_name= translit(document, language_code='ru', reversed=True)
        zip_name = f'{translit_doc_name}.zip'
        zip_path = f'{settings.MEDIA_ROOT}/downloads/{zip_name}'
        archive = zipfile.ZipFile(zip_path, 'w')
        rootdir = os.path.basename(document_dir)

        for root, dir, files in os.walk(document_dir):
            for file in files:
                if file == document:
                    filepath = os.path.join(root, file)
                    parentpath = os.path.relpath(filepath, document_dir)
                    arcname = os.path.join(rootdir, parentpath)
                    archive.write(filepath, arcname)

        archive.close()


        if os.path.exists(zip_path):
            with open(zip_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream", )
                response['Content-Disposition'] = 'inline; filename=' + f'{zip_name}'
                return response
        raise Http404


# @TheSleepyNomad
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'main/project.html'
    context_object_name = 'project'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Проект'
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'main/projects.html'
    context_object_name = 'projects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Компании'
        return context
