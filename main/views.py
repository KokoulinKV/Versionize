import os
import zipfile

from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from transliterate import translit

from Versionize import settings
from main.forms import DocumentForm, AddSectionForm, CreateProjectForm
from main.models import Section, Company, Document, Project

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
        context['document'] = DocumentForm(instance=self.request.document)
        context['add_section'] = AddSectionForm(instance=self.request.add_section)
        context['create_project'] = CreateProjectForm(instance=self.request.create_project)
        # context['next_form'] = NextForm(instance=self.request.next_form)
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'doc_form': DocumentForm(prefix='doc_form_pre'),
             'add_section_form': AddSectionForm(prefix='add_section_form_pre'),
             'create_project_form': CreateProjectForm(prefix='create_project_form_pre')})
        # return self.render_to_response({'doc_form': DocumentForm(prefix='doc_form_pre'),
        #                                  'next_form': NextForm(prefix='next_form_pre')})

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        add_section_form = _get_form(request, AddSectionForm, 'add_section_form_pre')
        create_project_form = _get_form(request, CreateProjectForm, 'create_project_form_pre')
        
        if request.method == 'POST' and ajax_check(request):
            project_id = request.POST.get('project_id', None)
            request.session['active_project_id'] = project_id
            
        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.save()
                doc_form.data = clear_form_data(doc_form.data)
            except ValidationError:
                errors = 'Данная версия документа уже была загружена. Загрузите корректную новую версию.'
                # TODO Подумать как записывать ошибки нескольких форм
                return self.render_to_response({
                    'doc_form': doc_form,
                    'errors': errors
                })
        elif add_section_form.is_bound and add_section_form.is_valid():
            add_section_form.save()
            add_section_form.data = clear_form_data(add_section_form.data)

        elif create_project_form.is_bound and create_project_form.is_valid():
            create_project_form.save()
            create_project_form.data = clear_form_data(create_project_form.data)
        # elif next_form.is_bound and next_form.is_valid():
        # next_form.save()
        return self.render_to_response({'doc_form': doc_form,
                                        'add_section_form': add_section_form,
                                        'create_project_form': create_project_form})
        # return self.render_to_response({'doc_form': doc_form}, {'next_form': next_form})


class TotalListView(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get_queryset(self):
        queryset = Section.objects.filter(
            project_id=self.request.session['active_project_id'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Сводная таблица проекта'
        context['document'] = DocumentForm(instance=self.request.document)
        context['add_section'] = AddSectionForm(instance=self.request.add_section)
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'doc_form': DocumentForm(prefix='doc_form_pre'),
             'add_section_form': AddSectionForm(prefix='add_section_form_pre'),
             'object_list': self.get_queryset()})

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        add_section_form = _get_form(request, AddSectionForm, 'add_section_form_pre')
        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.save()
                doc_form.data = clear_form_data(doc_form.data)
            except ValidationError:
                errors = 'Данная версия документа уже была загружена. Загрузите корректную новую версию.'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'errors': errors
                })
        elif add_section_form.is_bound and add_section_form.is_valid():
            add_section_form.save()
            add_section_form.data = clear_form_data(add_section_form.data)

        return self.render_to_response({'doc_form': doc_form,
                                        'add_section_form': add_section_form,
                                        'object_list': self.get_queryset()})


class SectionDetailView(LoginRequiredMixin, DetailView):
    model = Section
    template_name = 'main/section.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'doc_form': DocumentForm(prefix='doc_form_pre'), 'section': self.get_object()})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Раздел'
        context['document'] = DocumentForm(instance=self.request.document)
        return context

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.save()
                # Чистим форму от введенных данных
                doc_form.data = {
                    'doc_form_pre-status': '',
                    'doc_form_pre-name': '',
                    'doc_form_pre-section': '',
                    'doc_form_pre': ''
                }
            except ValidationError:
                errors = 'Данная версия документа уже была загружена. Загрузите корректную новую версию.'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'errors': errors
                })
        return self.render_to_response({'doc_form': doc_form, 'section': self.get_object()})


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

