# -*- coding:UTF-8 -*-
import datetime
from simulator import models
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
                messages.add_message(self.request, messages.INFO, 'pas de panier pour cart_id.%s' % err.message)
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
        cart = models.CartOf.objects.create(creation_date=datetime.datetime.now(), created_by = self.request.user.username)
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


class CartDemandeAppro(Cart):
    """
    Panier viruel pour preparer la demande
    d'appro
    """
    def __init__(self, request):
        # Cart.__init__(request)
        super(CartDemandeAppro, self).__init__(request)
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


    def calcul_demande_appo(self, of):
        # calcul DA
        # 1- recherche du numero de la fiche
        code_formule = of.code_form_cond_id
        code_fiche = planif_models.DjangoFiche.objects.get(codecndt=code_formule)

        # 2 - recherche de la formule
        sql = """
                SELECT *
                FROM fcondt{}
                WHERE codecndt = {}
                AND codeprod IS NOT NULL
                ORDER BY ligncndt
                """.format(code_fiche , code_formule)

        all_columns, formule_cond_rows =  dictfetchall(sql)
        product = []
        tab_coef_cond  = []

        for elem in formule_cond_rows :
            if elem['codeprod']is not u"" :
                product.append(elem['codeprod'])
                tab_coef_cond.append(float(elem['nbrecndt']) )

        # 3- calcul
        # sort inverse de coef
        ligne = 0
        #coef.sort(reverse = False)
        formule = zip(product, tab_coef_cond)
        # messages.add_message(self.request, messages.INFO, 'formule  %s ' % (formule) )

        # 2 autre calcul
        ligne = 0
        proposition_2 = []
        coef_total  = 1
        # 1 er lecture de la table des goupes DTECONDT

        # 1 ieme lecture:
        ligne = 10
        tab_qtt_groupe , tab_coef_total , t_test = [],[],[]

        qtt_groupe_precedant = 1

        for product, coef in formule:
            #coef_total = coef_total * coef
            coef = int(coef)
            t_test.append(coef)

            if ligne == 10:
                ligne_actu = 10
                tab_qtt_groupe.append(coef)
                coef_total = 1
                tab_coef_total.append(coef_total)

            elif ligne == int(code_fiche.ligpart1) \
                or  ligne == int(code_fiche.ligpart2) \
                or ligne == int(code_fiche.ligpart3) \
                or ligne == int(code_fiche.ligpart4)  :
                # changement de groupe
                if coef == 0 :
                    tab_qtt_groupe.append(1)
                    qtt_groupe_precedant = 1
                else :
                    tab_qtt_groupe.append(coef)

                # coef_total
                # coef_total *  avant dernier qtt_groupe
                coef_total = coef_total * tab_qtt_groupe[len(tab_qtt_groupe) -2]
                tab_coef_total.append(coef_total)

            else :
                # tab_qtt_groupe reprend le dernier qtt_groupe
                tab_qtt_groupe.append(tab_qtt_groupe[len(tab_qtt_groupe) - 1])
                tab_coef_total.append(coef_total)

            # qtt_groupe_precedant
            try :
                product_obj = planif_models.DjangoProduit.objects.get(codeprod=product)
            except Exception as err:
                return None

            proposition_2.append(models.Dict2Obj(
                {
                'ligne' : ligne,
                'produit' : product_obj ,
                'coef' : coef,
                'coef_total' : coef_total,
                'quantite' : long(math.ceil( of.quantite_prevue / coef_total))
                }
                    )
                )
            # save precedant et suivant
            qtt_groupe_precedant = coef
            ligne = ligne + 10
            nomenc = [(elem.produit, elem.quantite) for elem in proposition_2]



        # return
        # messages.add_message(self.request, messages.INFO, 'proposition_2= %s' % (nomenc))

        result = {'code_of' : of.code_of, 'proposition' : proposition_2}
        return  models.Dict2Obj(result)
