from django.shortcuts import render


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
