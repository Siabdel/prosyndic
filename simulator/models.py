# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.conf import settings
from django.utils.html import format_html

class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
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
    valeur = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at  = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta :
        abstract = True 

# ------------------------------------
# -- Abstarct Service
# -----------------------------------
class Service(AbstractProduct):
    pass

# ------------------------------------
# -- CART (Panier d'articles) 
# -----------------------------------
class Cart(models.Model):
    
    class StatusChoice(models.TextChoices):
        ACTIVE = 'ACT', _('Encours')
        CLOS = 'CLO', _('cloturé'), 
    titre       = models.CharField(max_length=50, blank=True, null=True)
    statut      = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.ACTIVE) # 1- encours 2- Cloturee
    created_at     = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    comment     = models.TextField(null=True, default=None)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-created_at',)

    def __str__(self):
        return self.pk

# ------------------------------------
# -- ITEM du panier 
# ------------------------------------
class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'post' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class AbstractItem(models.Model):
    #cart = models.ForeignKey(AbstractCart, on_delete=models.CASCADE)
    #product = models.ForeignKey(AbstractProduct, verbose_name=_('Product'), on_delete=models.CASCADE)
  
    # entite 1 cart
    content_type_1   = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="entite_1")
    object_id_1      = models.PositiveIntegerField()
    content_object_1 = GenericForeignKey('content_type_1', 'object_id_1')
    # entite 2 product
    content_type_2   = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="entite_2")
    object_id_2      = models.PositiveIntegerField()
    content_object_2 = GenericForeignKey('content_type_2', 'object_id_2')

    quantity = models.IntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = ItemManager()

    def create_relation(self, obj):
        self.content_object_1 = obj
        self.save()
    
    class Meta:
        verbose_name = _('AbstactItem')
        ordering = ('-created_at',)
        abstract = True

    def __str__(self):
        return self.product.name

class Item(AbstractItem):
    @property
    def total_price(self):
        return self.quantity * self.unit_price

#----------------------------------------------------------------------------------
# DEVIS 
#----------------------------------------------------------------------------------
class Devis(Service):
    duration_days = models.IntegerField(_("duree de devis (jours)"), default=30)
    
    def deadline(self):
        aujourdhui = datetime.datetime.now()
        datefin = aujourdhui + datetime.timedelta(self.duree_jours)
# ------------------------------------
# -- Simulation de DEVIS 
# -----------------------------------
class PosteItem(Item):
    devise = models.CharField(max_length=50, blank=True, null=True)
        
    class Meta:
        verbose_name = _('poste')
        verbose_name_plural = _('postes')
        #ordering = ('product',)
    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)
