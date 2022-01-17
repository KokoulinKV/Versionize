from django.urls import path

# !Дать нормальные названия, передалть в cbv
from main.views import index, document, company, section, total, index2, document2, company2, section2, total2

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    # path('lk/', lk, name='lk'),
    # path('logout/', logout, name='logout'),

    # Для проверки отображения
    path('company/', company, name='company'),
    path('document/', document, name='document'),
    path('section/', section, name='section'),
    path('total/', total, name='total'),
    path('new_lk/', index2, name='index2'),
    path('company2/', company2, name='company2'),
    path('document2/', document2, name='document2'),
    path('section2/', section2, name='section2'),
    path('total2/', total2, name='total2'),
]
