# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django_pandas.managers import DataFrameManager
# class machine   conditionnement   gestform ""
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# from ofschedule.models import DjangoMachine
from django.conf import settings


class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """

    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])



#-------------------------------
#-- Cart panier
#-------------------------------

class CartOf(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'), auto_now_add=True)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.pk)

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    cart = models.ForeignKey(CartOf, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    # product as generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    #created    = models.DateTimeField(auto_now_add=True)
    #created_by = models.CharField(max_length=100)

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%s' % (self.pk)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)



#-------------------------------
#-- Cart article nomenclature
#-------------------------------

STATUT_DA = (
    ('1', 'encours'),
    ('2', 'Confirmee'),
    ('3', 'Cloturee'),
    ('4', 'annulee'),
   )

# ------------------------------------
# -- Simulation de la Demande Appro
# -----------------------------------
class DemandeApproSimulee(models.Model):
    statut      = models.CharField(max_length=1, choices=STATUT_DA, default="1") # 1- encours 2- Cloturee
    created     = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Enete Demande ApproSimulee Simulee')
        ordering = ('-created',)

    def clone(self, old):
        new_kwargs = dict([(fld.name, getattr(old, fld.name))
                           for fld in old._meta.fields if fld.name != old._meta.pk]);
        return self.__class__.objects.create(**new_kwargs)

    def __unicode__(self):
        return u'%s' % self.id


#------------------------------------
#-- la Commande d' Appro
#-----------------------------------
class DjangoCommandeApprov(models.Model):
    statut      = models.CharField(max_length=1, choices=STATUT_DA, default="1")
    created     = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)
    comment    = models.TextField(null=True, default=None)
    
    class Meta:
        verbose_name = _('Entete Commande approvisionnment')
        ordering = ('-created',)

    def __str__(self):
        return u'%s' % self.id



# ------------------------------------
# -- Simulation ligne de demande d'appro
# -----------------------------------
class LigneDemandeApproSimulee(models.Model):
    demande_appro  = models.ForeignKey(DemandeApproSimulee,
                                       verbose_name=_('demande appro simul'),
                                       related_name="mes_lignes",
                                       on_delete=models.CASCADE)
    item_cart   = models.ForeignKey(Item, verbose_name=_('item cart of'), on_delete=models.CASCADE)
    code_of     = models.CharField(max_length=25)
    #article     = models.ForeignKey(DjangoProduit, to_field='codeprod' , verbose_name=_('AC'))
    article         = models.CharField(max_length=4) # produit de la nomenclature
    nom_article     = models.CharField(max_length=100) # produit de la nomenclature
    commande        = models.CharField(max_length=6) # commande_client
    quantite_commandee    = models.IntegerField(verbose_name=_('quantite commandee'))
    quantite_prevue       = models.IntegerField(verbose_name=_('quantite prevue'))  # qte prevue of
    quantite_produit      = models.IntegerField(verbose_name=_('quantite produit')) # qte produit nomenclture
    quantite_panier       = models.IntegerField(verbose_name=_('quantite panier')) # qte saisie au panier
    #quantite_restante     = models.IntegerField(verbose_name=_('quantite restante')) # quantite restante
    selected              = models.BooleanField(default=False)
    validate              = models.BooleanField(default=False) # ligne validée dans une autre DA en CAS
    completed             = models.BooleanField(default=False)
    taux_perte_mp         = models.FloatField()

    class Meta:
        verbose_name = _('Ligne Demande Appro Simulee')
        unique_together = ("demande_appro", "code_of", "commande",  "article")

    def __unicode__(self):

        return u'%s-%s' % (self.item_cart, self.article)



# ------------------------------------
# -- Simulation ligne de demande d'appro
# -----------------------------------
class DjangoLigneCommandeApprov(models.Model):
    demande_appro  = models.ForeignKey(DjangoCommandeApprov,
                                       verbose_name=_('Commande approv'),
                                       related_name="lignes_cda",
                                       on_delete=models.CASCADE)
    code_of     = models.CharField(max_length=25)
    #article     = models.ForeignKey(DjangoProduit, to_field='codeprod' , verbose_name=_('AC'))
    article         = models.CharField(max_length=4) # produit de la nomenclature
    nom_article     = models.CharField(max_length=100) # produit de la nomenclature
    commande        = models.CharField(max_length=6) # commande_client
    quantite_commandee    = models.IntegerField(verbose_name=_('quantite commandee'))
    quantite_prevue       = models.IntegerField(verbose_name=_('quantite prevue'))  # qte prevue of
    quantite_produit      = models.IntegerField(verbose_name=_('quantite produit')) # qte produit nomenclture
    quantite_panier       = models.IntegerField(verbose_name=_('quantite panier')) # qte saisie au panier
    #quantite_restante     = models.IntegerField(verbose_name=_('quantite restante')) # quantite restante
    selected              = models.BooleanField(default=False)
    validate              = models.BooleanField(default=False) # ligne validée dans une autre DA en CAS
    completed             = models.BooleanField(default=False)
    taux_perte_mp   = models.FloatField()

    class Meta:
        verbose_name = _('Ligne Commande Appro')
        unique_together = ("demande_appro", "code_of", "commande", "article")

    def __unicode__(self):

        return u'%s' % (self.article)
