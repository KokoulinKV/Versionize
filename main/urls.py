from django.urls import path

from main.views import index, index2
from main.views import TotalListView, CompanyListView, SectionDetailView, DocumentDetailView

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('companies/', CompanyListView.as_view(), name='companies'),
    # path('company/<int:pk>', CompanyDetailView.as_view(), name='company'),
    path('document/<int:pk>', DocumentDetailView.as_view(), name='document'),
    path('section/<int:pk>', SectionDetailView.as_view(), name='section'),
    path('total/', TotalListView.as_view(), name='total'),
    path('new_lk/', index2, name='index2'),
]
