# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django_pandas.managers import DataFrameManager
# class machine   conditionnement   gestform ""
from django.contrib.auth.models import User
# from ofschedule.models import DjangoMachine
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from django.utils.translation import gettext_lazy as _



class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

# ------------------------------------
# -- Abstarct Product
# -----------------------------------
class AbstractProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    quantity_instock = models.IntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    active = models.BooleanField(default=True)
    created_at  = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta :
        abstract = True 

# ------------------------------------
# -- CART (Panier d'articles) 
# -----------------------------------

class CartOf(models.Model):
    class StatusChoice(models.TextChoices):
        ACTIVE = 'ACT', _('En cours')
        CLOS = 'CLO', _('Cloturé'), 

    titre = models.CharField(max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.ACTIVE)  # 1- encours 2- Cloturee
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    comment = models.TextField(null=True, blank=True)

    # Ajoutez cette ligne pour créer la relation avec ItemArticle
    items = models.ManyToManyField('ItemArticle', related_name='carts', blank=True)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('cartsOf')
        ordering = ('-created_at',)

    def __str__(self):
        return "{}".format(self.titre)


# ------------------------------------
# -- ITEM du panier 
# ------------------------------------

class ItemManager(models.Manager):
    def get_by_product(self, product):
        content_type = ContentType.objects.get_for_model(type(product))
        return self.get(content_type=content_type, object_id=product.pk)


    def get_product_item(self, obj_id):
        item = self.get(object_id=obj_id)
        return item.content_type.get_object_for_this_type(pk=item.object_id)


class ItemRaw(models.Model):
    raw_message = models.JSONField()

class ItemArticle(models.Model):    
    cart = models.ForeignKey('CartOf', on_delete=models.CASCADE, related_name='cart_items')
    created_at  = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField() 
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = ItemManager()

    class Meta:
        verbose_name = _('ItemArticle')
        verbose_name_plural = _('ItemArticles')
        ordering = ('-created_at',)
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price
   
    def set_product(self, product):
        self.content_object = product 
        self.object_id = product.pk
    
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)
   
    @property
    def product(self):
        return self.content_object

    @product.setter
    def set_product(self, value):
        self.content_type = ContentType.objects.get_for_model(type(value))
        self.content_object = value 
        self.object_id = value.product.pk 
    
    product = property(get_product, set_product) 
    
    def __str__(self):
        return "itemArticle : {}".format(self.product.name)

# ------------------------------------
# -- Abstarct Service & Produits
# -----------------------------------
class Product(AbstractProduct):
    pass
class Service(AbstractProduct):
    pass

#-------------------------------
#-- Cart article nomenclature
#-------------------------------

STATUT_DA = (
    ('1', 'encours'),
    ('2', 'Confirmee'),
    ('3', 'Cloturee'),
    ('4', 'annulee'),
   )
