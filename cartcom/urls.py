#-*- coding:utf-8 -*-
from django.urls import path, include
from django.conf import settings
from django.views.generic.list import ListView
from . import views as v_cartcom

pathpatterns = [
    # CART
    path('cart/(?P<action>[-\w]+)/$', v_cartcom.ListItemCartView.as_view(), name='list_item_incart'),
    path('console/listda/$', v_cartcom.crud_demande_appro, name='console_liste_da' ),
]