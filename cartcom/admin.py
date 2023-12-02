# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
from simulator import models as si_models

# Register your models here.

#-----------------
# demande appro
# ---------------
class DevisAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in si_models.Item._meta.get_fields()]
    #list_total.remove('id')
    list_display = list_total
    ordering = ['-datecdea']
    search_fields = [ 'cdeappro']
    list_display = [ 'cdeappro', 'cac_id', 'datecdea', 'pour_qui', 'a_qui', 'delapart', 'delai_ge' ]

#-----------------
# demande appro
# ---------------
class ItemLigneAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in si_models.Item._meta.get_fields()]
    list_total.remove('id')
    list_display = list_total
    #ordering = ['-datecdea']
    search_fields = [ 'cdeappro']
    list_display = ['cdeappro',  ]


# demande appro

# Cart
class CartAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in models.CartOf._meta.get_fields()]
    list_display = [ 'creation_date', 'created_by',  'checked_out'  ]

class ItemAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in models.Item._meta.get_fields()]
    list_display = [ 'id',  'object_id', 'quantity', 'unit_price'  ]


admin.site.register(models.CartOf, CartAdmin)
admin.site.register(models.Item, ItemAdmin)

# Demande appro simulee

class DemandeApproSimuleeAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.DemandeApproSimulee._meta.get_fields()]
    #list_display = list_total

    list_display = ['id', 'statut', 'created'  , 'created_by', 'entrepot', 'zone_appro' , 'semaine'  , 'annee', 'machine' ]


# Ligne de Demande appro simulee

class LigneDemandeApproSimuleeAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.LigneDemandeApproSimulee._meta.get_fields()]
    list_display = list_total
    #list_display = ['demande_appro', 'code_of', 'article', 'commande', 'machine', 'quantite_commandee', 'quantite_produit', 'selected']



# Demande appro simulee

class DjangoCommandeApproAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.DjangoCommandeApprov._meta.get_fields()]
    #list_display = list_total

    list_display = ['id', 'statut', 'created'  , 'created_by', 'entrepot', 'zone_appro' , 'semaine'  , 'annee', 'machine', 'comment']


# Ligne de Demande appro simulee

class DjangoLigneCommandeApproAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.DjangoLigneCommandeApprov._meta.get_fields()]
    list_display = list_total
    # list_display = ['demande_appro', 'code_of', 'article', 'commande', 'quantite_commandee', 'quantite_produit', 'selected']
    list_display = ['id', 'demande_appro', 'code_of', 'article', 'commande', 'quantite_commandee', 'quantite_produit', 'selected', 'validate']


admin.site.register(models.DemandeApproSimulee, DemandeApproSimuleeAdmin)
admin.site.register(models.LigneDemandeApproSimulee, LigneDemandeApproSimuleeAdmin)

admin.site.register(models.DjangoCommandeApprov, DjangoCommandeApproAdmin)
admin.site.register(models.DjangoLigneCommandeApprov, DjangoLigneCommandeApproAdmin)
