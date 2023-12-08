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
import cartcom.models as cart_models

class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

#------------------------
# DEVIS 
#------------------------
class Devis(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duration_days = models.IntegerField(_("duree de devis (jours)"), default=30)
    items_article = GenericRelation(cart_models.ItemArticle, null=True, blank=True) #  les commantaires rattachées
 
    
    def deadline(self):
        aujourdhui = datetime.datetime.now()
        datefin = aujourdhui + datetime.timedelta(self.duree_jours)
        
    class Meta:
        verbose_name = _('Devis')
        verbose_name_plural = _('Devis')
    
    # add  partenaire du project
    def add_item_article(self, content_item, v_action):
        article = cart_models.ItemArticle(
                            description=content_item,
                            content_object=self,
                            object_id=self.pk)
        article.save()

    # get partenaire du project
    def get_item_articles(self):
        return cart_models.ItemArticle.objects.filter(object_id=self.pk)

    # get pieces jointes au project
    def get_article(self):
        return self.items_article.all()

    def __str__(self):
        return "Devis : {}".format(self.title)

    
    