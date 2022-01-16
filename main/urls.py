from django.urls import path

# !Дать нормальные названия, передалть в cbv
from main.views import index, document, company, section, total, index2
from main.views import TotalListView

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    # path('lk/', lk, name='lk'),
    # path('logout/', logout, name='logout'),

    # Для проверки отображения
    path('company/', company, name='company'),
    path('document/', document, name='document'),
    path('section/', section, name='section'),
    path('total/', TotalListView.as_view(), name='total'),
    path('new_lk/', index2, name='index2'),
]
