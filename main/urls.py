from django.urls import path

# !Дать нормальные названия, передалть в cbv
from main.views import index, document, section, index2
from main.views import TotalListView, CompanyListView, SectionDetailView

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('companies/', CompanyListView.as_view(), name='companies'),
    # path('company/<int:pk>', CompanyDetailView.as_view(), name='company'),
    path('document/', document, name='document'),
    path('section/<int:pk>', SectionDetailView.as_view(), name='section'),
    path('total/', TotalListView.as_view(), name='total'),
    path('new_lk/', index2, name='index2'),
]
