from django.urls import path
from simulator import views
from .views import RubriqueListCreateView, SousRubriqueListCreateView, ChargesFonctionnementListCreateView


urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.ListItemCartView.as_view(), name="list_item"),
    ##
    path('rubriques/', RubriqueListCreateView.as_view(), name='rubrique-list-create'),
    path('sous-rubriques/', SousRubriqueListCreateView.as_view(), name='sous-rubrique-list-create'),
    path('charges-fonctionnement/', ChargesFonctionnementListCreateView.as_view(), name='charges-fonctionnement-list-create'),

]