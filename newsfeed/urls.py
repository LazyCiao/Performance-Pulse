from django.urls import path
from . import views

app_name = 'newsfeed'

urlpatterns = [
    path('news/', views.news, name='news'),
]