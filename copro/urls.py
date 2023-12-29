from django.urls import path, include
from copro import views
from copro import views as pro_view

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('services/', views.PortailHome.as_view(), name='home_page'),
    # API framework 
    ## API
    path('api/doc/',  pro_view.DocumentApiList.as_view(), ), # new
    path('api/syndic/',  pro_view.SyndicApiList.as_view(), ), # new
    path('api/pivote/', views.ApiCandidatPivotList.as_view(), name="piv_compare"),
    ## Vue.js
    path('basedoc/', views.BaseDonneeDoc.as_view(), name="basdoc"), # Document
    path('compare/', views.CompareViewList.as_view(), name="compare"),
    path('pivote/', views.CandidatPivotList.as_view(), name="piv_compare"),
] 