from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('financial_pulse/', include('financial_pulse.urls')),
    path('crypto_pulse/', include('crypto_pulse.urls')),
]