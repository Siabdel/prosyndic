# -*- coding:UTF-8 -*-
import datetime
from simulator import models
# from . import views as ofviews
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.models import User, AnonymousUser
import math
from . import models
from simulator import models as planif_models


CART_ID = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass


CART_ID = 'cart_id'  # Assurez-vous que CART_ID est défini dans votre code


from django.contrib import messages
from .models import CartOf, ItemArticle
from django.utils.translation import gettext_lazy as _

CART_ID = 'cart_id'  # Assurez-vous que CART_ID est défini dans votre code

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart_id = self.session.get(CART_ID)
        self.cartdb = None
        self.request = request

        if cart_id:
            try:
                self.cartdb = CartOf.objects.get(id=cart_id, checked_out=False)
            except CartOf.DoesNotExist:
                messages.add_message(self.request, messages.INFO, 'Pas de panier pour cart_id {}'.format(cart_id))
                try:
                    self.cartdb = CartOf.objects.filter(created_by=request.user).order_by('id').last()
                    request.session[CART_ID] = self.cartdb.pk
                except Exception as err:
                    messages.add_message(self.request, messages.INFO, 'Erreur: {}'.format(err))
                    self.cartdb = self.new(request)
        elif CartOf.objects.filter(created_by=request.user).exists():
            try:
                self.cartdb = CartOf.objects.filter(created_by=request.user).order_by('id').last()
                request.session[CART_ID] = self.cartdb.pk
            except Exception as err:
                messages.add_message(self.request, messages.INFO, 'Erreur: {}'.format(err))
        else:
            self.cartdb = self.new(request)

    def new(self, request):
        cart = CartOf.objects.create(created_by=request.user)
        request.session[CART_ID] = cart.id
        messages.add_message(self.request, messages.INFO, 'On crée un panier {}'.format(cart.id))
        return cart

    def add(self, product, quantity=1):
        
        try:
            ## item = ItemArticle.objects.filter(cart=self.cartdb, product=product )
            item = ItemArticle.objects.get_by_product(product)
            
        except ItemArticle.DoesNotExist:
            item = ItemArticle()
            item.cart = self.cartdb
            item.unit_price = product.unit_price
            item.quantity = quantity
            item.content_object = product
            item.object_id = product.pk
            messages.add_message(self.request, messages.INFO, '### try in add  {} ###'.format(product.id))
            item.save()
        else:
            item.unit_price = product.unit_price
            item.quantity += int(quantity)
            item.save()

    def remove(self, product):
        try:
            item = ItemArticle.objects.get(cart=self.cartdb, product=product)
        except ItemArticle.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        try:
            item = ItemArticle.objects.get(cart=self.cartdb, product=product)
        except ItemArticle.DoesNotExist:
            raise ItemDoesNotExist
        else:
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = int(quantity)
                item.save()

    def count(self):
        result = 0
        for item in self.cartdb.items.all():
            result += item.quantity
        return result

    def summary(self):
        result = 0
        for item in self.cartdb.items.all():
            result += item.total_price
        return result

    def clear(self):
        for item in self.cartdb.items.all():
            item.delete()

    def is_empty(self):
        return self.count() == 0

    def cart_serializable(self):
        representation = {}
        for item in self.cartdb.items.all():
            itemID = str(item.object_id)
            itemToDict = {
                'total_price': item.total_price,
                'quantity': item.quantity
            }
            representation[itemID] = itemToDict
        return representation

    def django_query_serializable(self, new_class, data):
        data_final = []

        for item in data:
            itemID = str(item.object_id)
            new_row = dict([(fld.name, item) for fld in new_class._meta.fields if fld.name != new_class._meta.pk])
            data_final.append(new_row)

        return data_final

#------------------
#-----
#------------------
class CartDevis(Cart):
    """
    Panier viruel pour preparer la commande
    """
    def __init__(self, request):
        # Cart.__init__(request)
        super(CartDevis, self).__init__(request)
        Cart.__init__(self, request)

    def get_car_count(self):
        if self.cartdb:
            return  self.cartdb.item_set.all().count()
        else:
            return 0

    def is_product_exist_incart(self, product):
        # messages.add_message(self.request, messages.INFO, 'type of self.cartdb  = %s ' %  self.cartdb.item_set.all())
        if type(self.cartdb ) == models.CartOf:
            for item in self.cartdb.cart_items.all():
                if item.product.pk == product.id:
                    return True
        return False
def create_cart_in_database( creation_date=datetime.datetime.now(), checked_out=False):
    """
        Helper function so I don't repeat myself
    """
    cart = models.CartOf()
    cart.creation_date = creation_date
    cart.checked_out = False
    cart.save()
    return cart

def create_item_in_database(cart, product, quantity=1, unit_price=Decimal("100")):
    """
        Helper function so I don't repeat myself
    """
    item = models.ItemArticle()
    item.cart = cart
    item.product = product
    item.quantity = quantity
    item.unit_price = unit_price
    item.save()

    return item

