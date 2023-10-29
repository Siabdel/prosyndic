from django.urls import path, include
from copro import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.PortailHome.as_view(), name='home_page'),
] 