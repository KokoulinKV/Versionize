from django.urls import path


from main.views import TotalListView, CompanyListView, SectionDetailView, DocumentDetailView, Index,index2, document2, company2, section2, total2


app_name = 'main'

urlpatterns = [
    path('user/<int:pk>', Index.as_view(), name='index'),
    path('companies/', CompanyListView.as_view(), name='companies'),
    # path('company/<int:pk>', CompanyDetailView.as_view(), name='company'),
    path('document/<int:pk>', DocumentDetailView.as_view(), name='document'),
    path('section/<int:pk>', SectionDetailView.as_view(), name='section'),
    path('total/', TotalListView.as_view(), name='total'),
  
  # Для проверки отображения
#     path('company/', company, name='company'),
#     path('document/', document, name='document'),
#     path('section/', section, name='section'),
#     path('total/', total, name='total'),
    path('new_lk/', index2, name='index2'),
    path('company2/', company2, name='company2'),
    path('document2/', document2, name='document2'),
    path('section2/', section2, name='section2'),
    path('total2/', total2, name='total2'),
]
