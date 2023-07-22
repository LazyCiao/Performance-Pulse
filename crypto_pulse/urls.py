from django.urls import path
from . import views

app_name = 'crypto_pulse'

urlpatterns = [
    path('crypto/', views.crypto, name='crypto'),
]