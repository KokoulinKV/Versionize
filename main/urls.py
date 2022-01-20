from django.urls import path

# !Дать нормальные названия, передалть в cbv
from main.views import TotalListView, CompanyListView, SectionDetailView, DocumentDetailView, Index

app_name = 'main'

urlpatterns = [
    path('user/<int:pk>', Index.as_view(), name='index'),
    path('companies/', CompanyListView.as_view(), name='companies'),
    path('document/<int:pk>', DocumentDetailView.as_view(), name='document'),
    path('section/<int:pk>', SectionDetailView.as_view(), name='section'),
    path('total/', TotalListView.as_view(), name='total'),
]
