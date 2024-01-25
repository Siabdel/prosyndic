#-*- coding:utf-8 -*-
from django.urls import path, include
from django.conf import settings
from django.views.generic.list import ListView
from cartcom import views as v_cartcom
from cartcom import api_view as api_cartcom

urlpatterns = [
    # CART
    path('', v_cartcom.home, name='home'),
    path('<slug:action>/<int:product_id>/', v_cartcom.ListItemCartView.as_view(), name='list_item_incart'),
    path('ajax/detail/<slug:action>/<int:pk>', v_cartcom.home, name='cart_select_article_ligneda'),
    ##
    path('home/<slug:action>/', v_cartcom.ListItemCartView.as_view(), name='product_list'),
    path('product/detail/<int:pk>/', v_cartcom.ListItemCartView.as_view(), name='product_detail'),
    path('addcart/<slug:action>/<int:product_id>/', v_cartcom.ListItemCartView.as_view(), name='add_product_tocart'),
    
    # API
    path('api/product/', api_cartcom.ProductApiList.as_view(), name='api_list_product'),
    
]