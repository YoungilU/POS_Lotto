from django.urls import path, include
from . import views

app_name = 'POSApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.stock, name='stock'),
]