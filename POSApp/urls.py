from django.urls import path, include
from . import views

app_name = 'POSApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.stock, name='stock'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name="logout"),
]