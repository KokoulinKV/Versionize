from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Section, Company, Document, User


class Index(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'main/lk2.html'


class TotalListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = 'main/total.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(project_id=self.request.session['active_project_id'])
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Сводная таблица проекта'
        return context


class SectionDetailView(LoginRequiredMixin, DetailView):
    model = Section
    template_name = 'main/section.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Раздел'
        return context


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


def company2(request):
    return render(request, 'main/company2.html')


def document2(request):
    return render(request, 'main/document2.html')


def section2(request):
    return render(request, 'main/section2.html')


def total2(request):
    return render(request, 'main/total2.html')
