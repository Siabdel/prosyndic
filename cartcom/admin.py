# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from cartcom import models as cart_models
from simulator import models as si_models
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms

# Register your models here.
#-----------------
# demande Item Article
# ---------------
@admin.register(cart_models.ItemArticle)
class ItemArticleAdmin(admin.ModelAdmin) :
    #list_total  = [ f.name for f in cart_models.ItemArticle._meta.get_fields()]
    list_display = [ 'cart', 'content_type',  'quantity', 'unit_price' , 'product', ]
    fields = [ 'cart',  'quantity', 'unit_price' ,  ]

class ItemArticleInlineAdmin(GenericTabularInline):
    model = cart_models.ItemArticle
    extra = 0
    

class ItemArticleAdminForm(forms.ModelForm):
    class Meta:
        model = cart_models.ItemArticle
        fields = '__all__'  # Keep all fields 
    
    def get_product(self, obj):
        return obj.product.titre

# Cart
@admin.register(cart_models.CartOf)
class CartAdmin(admin.ModelAdmin) :
    form = ItemArticleAdminForm
    inlines = [ItemArticleInlineAdmin]
    
    list_total  = [ f.name for f in cart_models.CartOf._meta.get_fields()]
    list_display = [ 'created_by',  'titre', 'checked_out', ]
    #fields = [ 'cart',  'quantity', 'unit_price' ,  ]

@admin.register(cart_models.Product)
class ProduitAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in cart_models.Product._meta.get_fields()]
    list_display = list_total

@admin.register(cart_models.Service)
class ServiceAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in cart_models.Service._meta.get_fields()]
    list_display = list_total
