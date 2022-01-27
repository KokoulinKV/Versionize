from django.urls import path

# !Дать нормальные названия, передалть в cbv
from main.views import TotalListView, CompanyListView, SectionDetailView, DocumentDetailView, Index, DocumentDownload, \
    DocumentDownloadAllOfTotal, DocumentDownloadAllOfSection, ProjectDetailView


app_name = 'main'

urlpatterns = [
    path('user/<int:pk>', Index.as_view(), name='index'),
    path('companies/', CompanyListView.as_view(), name='companies'),
    path('document/<int:pk>', DocumentDetailView.as_view(), name='document'),
    path('section/<int:pk>', SectionDetailView.as_view(), name='section'),
    path('total/', TotalListView.as_view(), name='total'),
    path('document_download/<int:pk>', DocumentDownload.as_view(), name='document_download'),
    path('document_download_all/<int:pk>', DocumentDownloadAllOfTotal.as_view(), name='document_download_all'),
    path('document_download_all_section/<int:pk>', DocumentDownloadAllOfSection.as_view(), name='document_download_all_section'),
    path('project/<int:pk>', ProjectDetailView.as_view(), name='project'),
]
