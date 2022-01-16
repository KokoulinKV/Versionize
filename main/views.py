from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from main.models import Section, Company


def index(request):
    return render(request, 'main/lk.html')


# Проверка отображения новых шаблонов
def index2(request):
    return render(request, 'main/lk2.html')


def company(request):
    return render(request, 'main/companies.html')


def document(request):
    return render(request, 'main/document.html')


def section(request):
    return render(request, 'main/section.html')


def total(request):
    return render(request, 'main/total.html')


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
