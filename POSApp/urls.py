from django.urls import path, include
from . import views

app_name = 'POSApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.index, name='test'),
]