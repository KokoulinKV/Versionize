from django.urls import path

from main.views import TotalListView, CompanyListView, SectionDetailView, DocumentDetailView, Index

app_name = 'main'

urlpatterns = [
    path('/', Index.as_view(), name='index'),
    path('companies/', CompanyListView.as_view(), name='companies'),
    # path('company/<int:pk>', CompanyDetailView.as_view(), name='company'),
    path('document/<int:pk>', DocumentDetailView.as_view(), name='document'),
    path('section/<int:pk>', SectionDetailView.as_view(), name='section'),
    path('total/', TotalListView.as_view(), name='total'),
]
