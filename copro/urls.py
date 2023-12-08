from django.urls import path, include
from copro import views
from cartcom import api

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('home/', views.Home.as_view(), name='home'),
    path('services/', views.PortailHome.as_view(), name='home_page'),
    ## API
    path('basedoc/', views.BaseDonneeDoc.as_view(), name="basdoc"),
] 