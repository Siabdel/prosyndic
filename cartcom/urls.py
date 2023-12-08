#-*- coding:utf-8 -*-
from django.urls import path, include
from django.conf import settings
from django.views.generic.list import ListView
from cartcom import views as v_cartcom
from cartcom import api as api_cartcom

urlpatterns = [
    # CART
    path('', v_cartcom.home, name='home'),
    path('cart/<slug:action>/', v_cartcom.ListItemCartView.as_view(), name='list_item_incart'),
    path('ajax/detail/<slug:action>/<int:pk>', v_cartcom.home, name='cart_select_article_ligneda'),
    ##
    # API
    path('api/product/', api_cartcom.ProduitApiList.as_view(), name='api_list_product'),
    
]