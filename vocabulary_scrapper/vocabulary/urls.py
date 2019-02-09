from django.urls import path
from vocabulary import views

app_name = 'vocabulary'
urlpatterns = [
    path('', views.index),
    path('extract', views.extract, name='extract')
]
