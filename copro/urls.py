from django.urls import path, include
from copro import views
from copro import views as pro_view

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('home/', views.Home.as_view(), name='home'),
    path('services/', views.PortailHome.as_view(), name='home_page'),
    path('basedoc/', views.BaseDonneeDoc.as_view(), name="basdoc"), # Document
    path('doc/',  pro_view.DocumentApiList.as_view(), ), # new
    # API framework 
    
] 