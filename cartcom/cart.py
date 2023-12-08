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


class Cart(object):
    """
    Panier viruel
    """
    cardb = None
    def __init__(self, request):
        self.session = request.session
        cart_id = self.session.get(CART_ID)
        self.cartdb = None
        self.request = request

        # messages.add_message(self.request, messages.INFO, 'init objet cart_id.%s' % cart_id)
        cartDB = None
        if cart_id: # on trouve un dans la session
            try:
                self.cartdb = models.CartOf.objects.get(id=cart_id, checked_out=False)
            # except  models.CartOf.DoesNotExist:
            except Exception as err:
                messages.add_message(self.request, messages.INFO, 'pas de panier pour cart_id.%s' % err)
                try :
                    self.cartdb = models.CartOf.objects.filter( created_by = request.user).order_by('id').last()
                    # on update CART_ID en session
                    request.session[CART_ID] = self.cartdb.pk
                except Exception as err:
                    self.cartdb = self.new(request)

        # sinon dernier panier pour cet user
        elif models.CartOf.objects.filter(created_by = self.request.user).exists():
            try :
                self.cartdb = models.CartOf.objects.filter( created_by = self.request.user).order_by('id').last()
                messages.add_message(self.request, messages.INFO, ' sinon dernier panier pour cet user en base = %s' % self.cartdb)
                # on update CART_ID en session
                request.session[CART_ID] = self.cartdb.pk
            except Exception as err:
                messages.add_message(self.request, messages.INFO, 'Erreur dernier panier pour cet user en base = %s' % err.message)

        else:  # sinon on cree un nouveau panier
            self.cartdb= self.new(request)
            messages.add_message(self.request, messages.INFO, ' sinon on cree un nouveau panier %s' % self.cartdb.pk)


    def get(self, request,  *args,  **kwargs):
        self.object_list = models.CartOf.objects.all().group_by("-created")
        cart_id = request.session.get(CART_ID)
        return self.render()

    def __iter__(self):
        for item in self.cartdb.item_set.all():
            yield item

    def new(self, request):
        cart = models.CartOf.objects.create(creation_date=datetime.datetime.now(), created_by = self.request.user)
        cart.save()
        request.session[CART_ID] = cart.id
        messages.add_message(self.request, messages.INFO, 'on cree un panier .%s' % cart.id)
        return cart

    def add(self, product, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                cart=self.cartdb,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cartdb
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity += int(quantity)
            item.save()

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cartdb,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cartdb,
                product=product,
            )
        except Exception :
            #DoesNotExist:
            raise ItemDoesNotExist
        else: #ItemAlreadyExists
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = int(quantity)
                item.save()

    def count(self):
        result = 0
        for item in self.cartdb.item_set.all():
            result += 1 * item.quantity
        return result

    def summary(self):
        result = 0
        for item in self.cartdb.item_set.all():
            result += item.total_price
        return result

    def clear(self):
        for item in self.cartdb.item_set.all():
            item.delete()

    def is_empty(self):
        return self.count() == 0

    def cart_serializable(self):
        representation = {}
        for item in self.cartdb.item_set.all():
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
            #new_row = dict([(fld.name, getattr(item, fld.name))
            new_row = dict([(fld.name, item) for fld in new_class._meta.fields if fld.name != new_class._meta.pk ])
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

    def is_product_exist_incart(self, of):
        # messages.add_message(self.request, messages.INFO, 'type of self.cartdb  = %s ' %  self.cartdb.item_set.all())
        for item in self.cartdb.item_set.all():
            if item.product.code_of == of.code_of:
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
    item = models.Item()
    item.cart = cart
    item.product = product
    item.quantity = quantity
    item.unit_price = unit_price
    item.save()

    return item

