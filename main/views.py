# import PyPDF2 as PyPDF2
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms import DocumentForm
from main.models import Section, Company, Document


def _get_form(request, formcls, prefix):
    if prefix in request.POST:
        data = request.POST
        if request.FILES:
            files = request.FILES
            return formcls(data, files, prefix=prefix)
    else:
        data = None
    return formcls(data, prefix=prefix)

def _clean_form_data(form):
    new_data=form.data.copy()
    for v, k in new_data.items():
        if v!='csrfmiddlewaretoken':
            new_data[v] = ''
    form.data = new_data
    return form

class Index(LoginRequiredMixin, TemplateView):
    template_name = 'main/lk.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Сводная таблица проекта'
        context['document'] = DocumentForm(instance=self.request.document)
        # context['next_form'] = NextForm(instance=self.request.next_form)
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'doc_form': DocumentForm(prefix='doc_form_pre')})
        # return self.render_to_response({'doc_form': DocumentForm(prefix='doc_form_pre'),
        #                                  'next_form': NextForm(prefix='next_form_pre')})

    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        # next_form = _get_form(request, NextForm, 'next_form_pre')
        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.save()
                # Чистим форму от введенных данных
                doc_form=_clean_form_data(doc_form)
            except ValidationError:
                errors = 'Данная версия документа уже была загружена. Загрузите корректную новую версию.'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'errors': errors
                })
            # except TypeError:
            #     errors = 'Документ должен быть в формате ".pdf"'
            #     return self.render_to_response({
            #         'doc_form': doc_form,
            #         'errors': errors
            #     })
        # elif next_form.is_bound and next_form.is_valid():
        # next_form.save()
        return self.render_to_response({'doc_form': doc_form})
        # return self.render_to_response({'doc_form': doc_form}, {'next_form': next_form})


class TotalListView(LoginRequiredMixin, TemplateView):
    template_name = 'main/total.html'

    def get_queryset(self):
        queryset = Section.objects.filter(
            project_id=self.request.session['active_project_id'])
        return queryset

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'doc_form': DocumentForm(prefix='doc_form_pre'), 'object_list': self.get_queryset()})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Сводная таблица проекта'
        context['document'] = DocumentForm(instance=self.request.document)
        return context


    def post(self, request, *args, **kwargs):
        doc_form = _get_form(request, DocumentForm, 'doc_form_pre')
        if doc_form.is_bound and doc_form.is_valid():
            try:
                doc_form.save()
                # Чистим форму от введенных данных
                doc_form=_clean_form_data(doc_form)
            except ValidationError:
                errors = 'Данная версия документа уже была загружена. Загрузите корректную новую версию.'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'errors': errors
                })
        return self.render_to_response({'doc_form': doc_form, 'object_list': self.get_queryset()})

class SectionDetailView(LoginRequiredMixin, DetailView):
    model = Section
    template_name = 'main/section.html'
    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'doc_form': DocumentForm(prefix='doc_form_pre'),'section': self.get_object()})

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
                doc_form=_clean_form_data(doc_form)
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



