from django.urls import path
from . import views

app_name = 'financial_pulse'

urlpatterns = [
    path('search_company/', views.search_company, name='search_company'),
    path('social_media/', views.social_media, name='social_media'),
    path('company_data/', views.company_data, name='company_data')
]