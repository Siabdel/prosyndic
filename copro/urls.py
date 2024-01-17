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
    path('api/pivote/', pro_view.ApiCandidatPivotList.as_view(), name="apiv_compare"),
    path('api/indicateur/', views.ApiIndicateursList.as_view(), name="api_indic_compare"),
    ## Vue.js
    path('basedoc/', pro_view.BaseDonneeDoc.as_view(), name="basdoc"), # Document
    path('compare/', pro_view.CompareViewList.as_view(), name="compare"),
    path('pivote/', pro_view.CandidatPivotList.as_view(), name="piv_compare"),
    path('compare_indic/', pro_view.ComparateurIndicateurstList.as_view(), name="indicateur_compare"),
]
