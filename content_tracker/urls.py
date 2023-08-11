from django.urls import path
from . import views

app_name = 'content_tracker'

urlpatterns = [
    path('profile_search/', views.profile_search, name='profile_search'),
]