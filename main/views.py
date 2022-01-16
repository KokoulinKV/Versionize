from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from main.models import Section


def index(request):
    return render(request, 'main/lk.html')


# Проверка отображения новых шаблонов
def index2(request):
    return render(request, 'main/lk2.html')


def company(request):
    return render(request, 'main/company.html')


def document(request):
    return render(request, 'main/document.html')


def section(request):
    return render(request, 'main/section.html')


def total(request):
    return render(request, 'main/total.html')


class TotalListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = 'main/total.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Versionize - Сводная таблица проекта'
        return context
