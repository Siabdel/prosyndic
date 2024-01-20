from django.db import models
from django.contrib import admin
from simulator import models as ss_models
from cartcom import models as cart_models
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms
from django.contrib import admin
from .models import Rubrique, SousRubrique, ChargesFonctionnement

    
class ItemArticleInlineAdmin(GenericTabularInline):
    model = cart_models.ItemArticle
    extra = 1

class ItemArticleAdminForm(forms.ModelForm):
    class Meta:
        model = cart_models.ItemArticle
        fields = '__all__'  # Keep all fields 

# Register your Devis here.
""" 
Le devis est d'abord un document d'information qui 
matérialise l'engagement des parties et qui doit être signé avant la prestation. 
La facture quant à elle, intervient à l'issue de la prestation. 
Il s'agit avant tout d'un document comptable tant pour le prestataire 
que pour le client.
"""
@admin.register(ss_models.Devis)
class DevisAdmin(admin.ModelAdmin) :
    form = ItemArticleAdminForm
    inlines = [ItemArticleInlineAdmin]
    list_total  = [ f.name for f in ss_models.Devis._meta.get_fields()]
    list_display = list_total
    

admin.site.register(Rubrique)
admin.site.register(SousRubrique)
admin.site.register(ChargesFonctionnement)
