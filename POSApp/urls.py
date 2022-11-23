from django.urls import path, include
from . import views

app_name = 'POSApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.stock, name='stock'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]