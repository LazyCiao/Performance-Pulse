from django.urls import path
from . import views

app_name = 'crypto_pulse'

urlpatterns = [
    path('crypto/', views.crypto, name='crypto'),
    path('crypto/coin_chart/<str:coin_symbol>/', views.coin_chart, name='coin_chart'),
    path('crypto/coin_detail/<str:coin_name>/', views.coin_details, name='coin_details'),
    path('test/', views.test, name='test'),
]