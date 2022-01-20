import PyPDF2 as PyPDF2
from django.core.exceptions import ValidationError
from django.shortcuts import render
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
        None
    return formcls(data, prefix=prefix)


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'main/lk2.html'

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
                # Проверяем на .pdf
                PyPDF2.PdfFileReader(open(doc_form.files, "rb"))

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
            except TypeError:
                errors = 'Документ должен быть в формате ".pdf"'
                return self.render_to_response({
                    'doc_form': doc_form,
                    'errors': errors
                })
        # elif next_form.is_bound and next_form.is_valid():
        # next_form.save()
        return self.render_to_response({'doc_form': doc_form})
        # return self.render_to_response({'doc_form': doc_form}, {'next_form': next_form})


class TotalListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = 'main/total2.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(
            project_id=self.request.session['active_project_id'])
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering, )
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Сводная таблица проекта'
        return context


class SectionDetailView(LoginRequiredMixin, DetailView):
    model = Section
    template_name = 'main/section2.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Раздел'
        return context


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'main/companies2.html'

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


def company2(request):
    return render(request, 'main/company2.html')


def document2(request):
    return render(request, 'main/document2.html')


def section2(request):
    return render(request, 'main/section2.html')


def total2(request):
    return render(request, 'main/total2.html')
