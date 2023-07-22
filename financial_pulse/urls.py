from django.urls import path
from . import views

app_name = 'financial_pulse'

urlpatterns = [
    path('search/', views.search_company, name='search'),
    path('test/', views.test, name='test'),
    path('company_data/', views.company_data, name='company_data')
]