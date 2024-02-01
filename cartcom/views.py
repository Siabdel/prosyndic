# -*- coding:UTF-8 -*-
import dateutil.parser
import os
import csv
import random
import logging
import pytz
import json
import io
import base64
import math

import numpy as np
from django_pandas.io import read_frame
import pandas as pd
from . import views as of_views
# from dateutil.parser import *
from django.db import connection
import pandas as pd
from django.db.models import Count
import numpy as np
import datetime
import django
from django.middleware.csrf import get_token
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, reverse
from django.views.generic.edit import UpdateView, CreateView, DeleteView, ModelFormMixin, ProcessFormView, FormView, FormMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from urllib.parse import quote
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from cartcom import forms
from cartcom import cart as e_cart
from cartcom import models as cart_models

# Rendez-vous

TIMEZONE = 'Europe/Paris'
# How long ago the timestamp is
# See timedelta doc http://docs.python.org/lib/datetime-timedelta.html
#since = datetime.datetime.utcnow() - date
now = datetime.datetime.utcnow()
now = now.replace(tzinfo=pytz.utc)
tz = pytz.timezone(TIMEZONE)

# Get an instance of a logger
logger = logging.getLogger(__name__)

#Django listview as JSON and Jquery getJSON example

def home(request):
    return HttpResponse("C'est Home ...")
                        
#  la liste des ofs
@method_decorator(login_required, 'dispatch')
class ListOfsView(ListView, FormView, e_cart.Cart):
    template_name = "list_of.html"
    paginate_by = 10  # if pagination is desired
    ## form_class = forms.SearchMachineForm
    object_list = None

    def __init__(self,  **kwargs):
        """
        contructeur avec Cart
        """
        super(ListOfsView, self).__init__(**kwargs)

    def get_context_data(self,  **kwargs):
        context = super(ListOfsView, self).get_context_data(**kwargs)
        # semaine actuelle
        semaine_aujourdhui = datetime.datetime.isocalendar(datetime.datetime.now())[1]
        img_choice = random.choice(range(10))
        #context['form'] = self.form_class
        form = forms.SearchMachineForm()
        # form.initial.update( {'user': self.request.user, 'cle_recherche': v_semaine})
        return context

    def get_form_kwargs__(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(ListOfsView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self, **kwargs):
        v_semaine = kwargs.get('semaine')
        v_annee = kwargs.get('annee')
        v_machine = kwargs.get('code_machine')
        messages.add_message(self.request, messages.INFO,
                             '**kwrag**=%s' % v_semaine)

        self.object_list = planif_models.DjangoOf.objects.filter(statut__in=['P', 'D'],
                                                          semaine=v_semaine,
                                                          annee=v_annee)
        #self.object_list = planif_models.DjangoOf.objects.all()
        return self.object_list

    def post__(self, request, *args, **kwargs):
        """
        """
        # 1/ on va recperer les criteres saisie pour selectionner les ofs
        jr_choisies = []
        jours_semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']

        form = forms.SearchMachineForm(request.POST)
        #form.is_valid()
        messages.add_message(self.request, messages.INFO, 'je suis dans post kwrag=%s' % request.POST.keys())
        # on verifie si le formulaire est valide
        if request.method == 'POST' and form.is_valid() :
            # 2/ on récupere la semaine, annee, et machine saisie par l'utilsateur
            machine = request.POST["machines"]
            semaine = request.POST["semaines"]
            jours_semaine   = request.POST["jours_semaine"]
            annee = kwargs.get('annee', None)
            #machine = form.cleaned_data["machines"]
            # on recupere les jour de destinations
            #
            for jour in request.POST.getlist('jours_semaine') :
                    jr_choisies.append(jour)

            # 3/ save les elements et on relance la recherche des ofs
            self.object_list = planif_models.DjangoOf.objects.filter(statut__in=['P'],
                                                              semaine=semaine,
                                                              annee=annee,
                                                              machine_travail_id = machine)

            # 4/ test si OF est deja concerné par une Cac
            self.object_list= list(self.object_list)
            for index, of in  enumerate(self.object_list):
                if not models.DjangoLigneCommandeApprov.filter(product_id=of.product_id).exists():
                    messages.add_message(self.request, messages.INFO, 'Of completed DA=%s' % of.product_id)
                    of.completetd=True



            #return HttpResponse("ok" + '---'.join(jours_semaine))
            #return self.form_invalid(form)
            return render(request, self.template_name, locals())

        else :
            # return
            erreurs = [ field.errors for field in form ]
            return render(request, self.template_name, locals())


    def render_json_response(self, queryset):
        """
        export json format
        """
        json_data = serializers.serialize('json', queryset)
        # Proceed to create your context object containing the columns and the data
        return HttpResponse(json_data, content_type='application/json')

    def api_simulation_demande_approv(self):
        # 0- recuperer les ofs du panier
        propositions = []
        mes_articles_of = self.cartdb.item_set.all()

        new_da_simu = models.DemandeApproSimulee.objects.get(pk=214)

        # 4 afficher la proposition
        all_columns = ['demande_appro', 'product_id', 'article', 'commande',
                       'machine', 'quantite_commandee', 'quantite_produit', 'selected']

        lignes_da = new_da_simu.mes_lignes.all()
        #.values_list( 'demande_appro', 'product_id', 'article', 'commande', 'machine', 'quantite_commandee', 'quantite_produit', 'selected' )
        #lignes_da  = models.LigneDemandeApproSimulee.objects.filter(demande_appro = 110)
        # messages.add_message(self.request, messages.INFO, 'lignes DA = %s' % lignes_da)

        json_data = serializers.serialize('json', lignes_da)
        #return self.render_json_response(lignes_da)

        data_test = {"products":[{"id":1,"quantity":1,"name":"Compass"},
                                 {"id":2,"quantity":0,"name":"Jacket"},
                                 {"id":3,"quantity":5,"name":"Hiking Socks"},
                                 {"id":4,"quantity":2,"name":"Suntan Lotion"}]}

        return json_data

    def get(self, request,   **kwargs):
        # on recupere le contexte
        self.request = request
        data = ""

        # initialisation objet panier
        Cart.__init__(self, request)
        #

        #self.object_list = planif_models.DjangoOf.objects.filter(semaine=v_semaine, annee=v_annee)
        self.get_queryset(**kwargs)
        #messages.add_message(None, messages.INFO, 'init objet cart_id.%s' % kwargs)
        v_semaine = kwargs.get('semaine')
        v_annee = kwargs.get('annee')
        v_machine = kwargs.get('code_machine')

        product_id = kwargs.get('product_id')
        quantitee = abs(float(kwargs.get('quantitee', 0)))

        action = kwargs.get('action')

        if action == "simvuejs":
            context = self.simulation_demande_approv(kwargs)
            return render(self.request, "propos_da_vues.html", locals())

        elif action == "selecteditem":
            item_id = kwargs.get('lda_pk')
            self.ajax_select_article_ligneda(item_id)

        # return si request est de type ajax on return une reponse json sino return response http
        # context = super(ListOfsView, self).get_context_data(**kwargs)
        context = self.get_context_data(**kwargs)

        if request.is_ajax():
            return JsonResponse(data, status=200, safe=False)
        else:
            return self.render_to_response(context)

    # ---------------
    # -- return to sender
    # ---------------
    def return_to_sender(self):
        return HttpResponseRedirect(reverse('list_of_view', kwargs={'semaine': 38, 'annee': 18}))

    # --------------------------
    # --ajax cart validate DA
    # ---------------------------
    def ajax_cart_validate_da(self, da_pk):
        """
        Update ligne DA SELECTED
        """
        resp = {}
        try:
            models.DemandeApproSimulee.objects.filter(pk=da_pk).update(statut=3)
            resp['status'] = "OK pk = %s  " % (da_pk)
            return da_pk

        except Exception as err:
            resp['status'] = "KO pk=%s  " % (self.request.GET.get('lda_pk', 0))

        return json.dumps(resp)

    # -------------------------------
    # --ajax select article ligneda
    # ------------------------------
    def ajax_select_article_ligneda(self, lda_pk):
        """
        Update ligne DA SELECTED
        """
        resp = {}
        try:
            lda = models.LigneDemandeApproSimulee.objects.get(pk=lda_pk)
            select_val = not lda.selected
            models.LigneDemandeApproSimulee.objects.filter(
                pk=lda_pk).update(selected=select_val)

            resp['status'] = "OK pk=%s  " % (select_val)

        except Exception as err:
            resp['status'] = "KO pk=%s  " % (self.request.GET.get('lda_pk', 0))

        return json.dumps(resp)

    def django_query_serializable(self, data):
        data_final = []
        new_class = data.first().__class__
        for item in data:
            itemID = str(item.object_id)
            # new_row = dict([(fld.name, getattr(item, fld.name))
            new_row = dict([(fld.name, item)
                            for fld in new_class._meta.fields if fld.name])
            data_final.append(new_row)

        return data_final
# -----------------------------------------
#  class Cart List items
# -----------------------------------------
@method_decorator(login_required, 'dispatch')
class ListItemCartView(ListView, e_cart.CartDevis):
    """
    details des produits nomenclature de DAS
    """
    #template_name="details_das.html"
    template_name="product_list.html"
    object_list = None
    form_class = forms.SearchMachineForm
    # paginate_by = 10  # if pagination is desired


    def __init__(self,  **kwargs):
        """
        contructeur avec Cart
        """
        super(ListItemCartView, self).__init__(**kwargs)

    def get_context_data(self,  **kwargs):
        context = super(ListItemCartView, self).get_context_data(**kwargs)
        # init panier Cart
        e_cart.Cart.__init__(self, self.request)
        ## messages.add_message(self.request, messages.INFO, 'in get_context_data cartdb= %s' % self.cartdb)
        
        # context['object_list'] = self.get_items_cart()
        context['products'] = cart_models.Product.objects.all()
        return context


    def get(self, request, *args, **kwargs):
        # on recupere le contexte
        self.request = request
        # initialisation objet panier
        # on recupere le context
        context = self.get_context_data(**kwargs)
        #-------------------------
        action = kwargs.get('action', 'listitem')
        
        product_id = kwargs.get('product_id',)
        ## messages.add_message(self.request, messages.INFO, '## in get = {} ##'.format(product_id))
        product = get_object_or_404(cart_models.Product, pk=product_id)
        quantitee = kwargs.get('quantitee', 1)

        if action == "listitem":
            context = self.get_context_data(**kwargs)
            context['item_list'] = self.get_list_items(context)
            messages.add_message(self.request, messages.INFO, 'in get()= %s' % self.cartdb)
            return render(self.request, "cart.html", context)

        elif action == "additem" and product_id:
            # ajout of dans panier
            data = self.add_item_of_incart(product, quantitee)
            ## messages.add_message(self.request, messages.INFO, 'add item in cart= %s' % self.cartdb)

        elif action == "delitem":
            item_id = kwargs.get('element_id')
            self.del_item_incart(item_id )
            return HttpResponseRedirect(reverse('list_item_incart', args=['listitem']))
            #return render(self.request, "cart.html", locals())

        elif action == "emptycart":
            item_id = kwargs.get('element_id')
            self.empty_cart()
            return HttpResponseRedirect(reverse('da_home_of'))

        elif action == "simulation":
            context = self.get_context_data(**kwargs)
            das_id = self.simulation_demande_approv(context)
            #return render(self.request, "proposition_da.html", context)
            return HttpResponseRedirect( reverse('das_action_details_product', args=[das_id]) )

        elif action == "apida":
            context = self.api_simulation_demande_approv()
            return HttpResponse(context)

        elif action == "count_cart":
            resp = {}
            resp['cart_count'] = self.get_car_count()
            response = HttpResponse(json.dumps(resp), content_type="application/json")
            return response

        elif action == "validateda":

            dem_appro_pk = kwargs.get('element_id')
            # data = self.ajax_cart_validate_da(dem_appro_pk)
            # if data:
            # 1 creer une commande DA valider
            messages.add_message(self.request, messages.INFO, 'on valide DA {}   !'.format(kwargs))

            try:
                da_courante = models.DemandeApproSimulee.objects.get( pk=dem_appro_pk)
                new_cac = self.transforme_cart_commande_da(da_courante)
            except Exception as err:
                messages.add_message(self.request, messages.INFO, 'Erreur DA {} introuvable !'.format(dem_appro_pk))
                return HttpResponseRedirect(reverse('list_item_incart', args=['listitem']))

            # 3- Creation Demande Appro GESTFORM
            self.create_da_gestform(new_cac.pk)

            # 3- suppression de la DAS
            try:
                self.cartdb.delete()
            except Exception as err:
                messages.add_message(self.request, messages.INFO, 'Erreur DA {} impossible a supprimer  !'.format(dem_appro_pk))
                return HttpResponseRedirect(reverse('list_item_incart'))

            # 4- vider le panier
            self.empty_cart()
            return JsonResponse({'new_cac:new_cac'}, status=200, safe=False)
            #return HttpResponseRedirect("/of/cac/list/")


        return self.render_to_response(context)
        #return self.get(args, **kwargs)

    # --
    def get_items_cart(self):
        """
        return list des items
        """
        return self.cartdb.item_set.all()

    # liste des item panier
    def get_list_items(self, context):
        item_list = []
        #
        try:
            item_list = cart_models.ItemArticle.objects.filter(cart=self.cartdb)
            # messages.add_message(self.request, messages.INFO, 'je vais dans le panier')
        except Exception as err:
            messages.add_message(self.request, messages.INFO,
                                 'Erreur list panier = %s ' % str(err))
        return item_list

    # ajout de of dans le panier
    def add_item_of_incart(self, product, quantitee=1):
        resp = {}
        try:
            ## if not self.is_product_exist_incart(product):
            # on ajoute dans panier
            self.add(product, quantitee)
            resp['status'] = "OK of ajouter dans panier = {}".format(product)
        except Exception as err:
            messages.add_message(self.request, messages.INFO, 'Erreur add product {} err={}'
                                 .format(product, err))
            resp['status'] = "KO error=%s  " % (str(err))

        return resp

    def del_item_incart(self, item_id):
        try :
            ii = cart_models.ItemArticle.objects.get(id=item_id)
            ii.delete()
        except Exception as err:
            messages.add_message(self.request, messages.INFO, 'Erreur del_item_incart = %s ' % item_id)
            pass


    def empty_cart(self):
        ii = cart_models.CartOf.objects.get(id=self.cartdb.id)
        ii.delete()

    def simulation_devis(self, context):
        # 0- recuperer les ofs du panier
        propositions = []
        return True

    # -------------------------------------------------
    # -- copy cart simulé en commande appro confirmée
    # --------------------------------------------------
    def transforme_cart_commande(self, old):
        # 1 creation entete commande approv
        demande_pa_pk = old.pk
        old_lignes = old.mes_lignes.all()
        old.pk = None
        new_cda = clone_row_indb(old, models.DjangoCommandeApprov)
        new_cda.statut = 2
        new_cda.save()

        # 2 creation lignes  commande approv
        # reactiver la demande cda
        old_cda = models.DemandeApproSimulee.objects.get(pk=demande_pa_pk)

        messages.add_message(self.request, messages.INFO, 'transforme_cart_commande_da=%s ' % (demande_pa_pk))

        for ligne in old_cda.mes_lignes.all():
            #ligne.pk = None
            defaults = {'demande_appro': new_cda}
            # que pour les ligne selected par user
            if ligne.selected:
                try:
                    new_ligne_cda = clone_row_indb(
                        ligne, models.DjangoLigneCommandeApprov, defaults)
                    # save
                    new_ligne_cda.demande_appro = new_cda
                    new_ligne_cda.validate = True
                    new_ligne_cda.selected = False
                    new_ligne_cda.completed = False
                    """
                    # verificatin si ce produit est complet
                    if is_quantite_prevue_completed(new_ligne_cda.product_id) :
                        new_ligne_cda.completed = True
                    elif (get_sum_quantite_panier(new_ligne_cda.product_id) > 0) and (get_sum_quantite_panier(new_ligne_cda.product_id) < cac.quantite_pprevue) :
                        #new_ligne_cda.completed = False
                        self.object_list[index].quantite_prevue = self.object_list[index].quantite_prevue - cac.quantite_panier
                    """
                    # save cac
                    new_ligne_cda.save()

                except IntegrityError as err:
                    if 'unique constraint' in err.message:
                        msg = 'unique constraint'
                    messages.add_message(self.request, messages.INFO,
                        'Erreur transforme_cart_commande_da: %s' % (err.message ))

                except Exception as err:
                    messages.add_message(self.request, messages.INFO,
                        'Erreur transforme_cart_commande_da: %s new_cde=%s' % (err.message , new_cda))

        return new_cda

#-----------------------
# Produit Details   
#-----------------------
def product_detail(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    return render(request, "store/product_detail.html", locals())


#-----------------------
# API Demande approv
#-----------------------

def api_add_item_of_incart(request, product_id):
    """
    add of in cart
    permettre d’associer un article au
    panier avec votre modèle de produit.
    """
    resp = {}
    user = request.user
    panier = request.session.get('CART_ID')
    messages.add_message(request, messages.DEBUG,
                         '%s mon panier in request.' % str(request.session))

    if not panier:
        panier = create_cart_in_database()
        request.session['CART_ID'] = panier.id
        #messages.add_message(request, messages.INFO, 'creation du panier %s' % str(panier ))

    # create_item_in_database(cart, product, quantity=1, unit_price=Decimal("100")):
    try:
        of = planif_models.DjangoOf.objects.get(product_id=product_id)
        #messages.add_message(request, messages.INFO, 'ajout de of dans le panier.%s' % product_id)
        messages.add_message(request, messages.INFO,  ' mon panier in request= %s ' % str(
            request.session.get('CART_ID')))
        item = create_item_in_database(panier, of)
    except Exception as err:
        messages.add_message(request, messages.INFO,
                             'Erreur dans add_item_of_incart: %s pour code of %s' % (str(err), product_id))

    resp['status'] = "OK"
    return HttpResponse(json.dumps(resp))

def api_list_cac(request, cac_id):
    """
    --
    """
    queryset  = models.DjangoLigneCommandeApprov.objects.filter(demande_appro=cac_id)
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

def api_demande_appro_sim(request):
    """
    API Demande approv
    """
    json_data = {}
    # 1- recuperer la demmande appro en cours pour cet user
    response = HttpResponse(content_type="application/json")
    if models.DemandeApproSimulee.objects.filter(created_by=request.user,
                                                     statut=1).exists():
        da_encours = models.DemandeApproSimulee.objects.filter( statut=1).first()

        # 2- calculer les DA pour charque of
        lignes_da = da_encours.mes_lignes.all().order_by("product_id")
        # lignes_da_json =  calcul_demande_appo_cumulee(9 )
        # messages.add_message(request, messages.INFO, 'Erreur dans api_demande_appro_sim %s' % (lignes_da_json))

        # 3 afficher la proposition
        serializers.serialize("json", lignes_da, stream=response)
        #json_data = serializers.serialize('json', lignes_da)
        #---------------
        # return HttpResponse(json.dumps(response_data), content_type="application/json")
        return response



#-----------------------
#  fonctions generic
#-----------------------

def clone_row_indb(old, new_class, defaults={}):
    new_kwargs = dict([(fld.name, getattr(old, fld.name))
                       for fld in new_class._meta.fields if fld.name != old._meta.pk])
    # and not issubclass(fld.name.__class__, object) ])
    # update dict avec default valeurs
    new_kwargs.update(defaults)
    return new_class.objects.create(**new_kwargs)


#  traite formulaire selection des produits
def traite_form_produit(request):
    #
    resp = {}
    resp = request.POST.get('id').strip()

    if request.method == 'POST':
        id = request.POST.get('id')
        existed = models.LigneDemandeApproSimulee.objects.filter(pk=id).exists()
        if existed:
            occurrence = models.LigneDemandeApproSimulee.objects.get(
                product_id=id)
            # save
            occurrence.quantite_prevue = request.POST.get(
                'quantite_prevue').strip()
            occurrence.save()
            resp['status'] = "OK"
        return HttpResponse(json.dumps(resp))


def update_object(obj, **kwargs):
    # new_instance = new_class.__class__()
    for k, v in kwargs.items():
        setattr(obj, k, v)
    obj.save(commit=False)

def is_quantite_prevue_completed(of):
    """
    """
    queryset = models.DjangoLigneCommandeApprov.objects.filter(product_id=of.product_id)

    ll = queryset.values_list('product_id', 'article').distinct()
    df = read_frame(ll, fieldnames=['product_id', 'quantite_panier', 'quantite_prevue'])
    # on sum la qte Panier
    dfg = df.groupby('product_id').sum()
    aa = dfg.aggregate('quantite_panier')
    # ---
    row = dict(aa.items())
    somme_qte_panier = int(row[queryset.first().product_id])
    return somme_qte_panier >= queryset.first().quantite_prevue


def get_sum_quantite_panier(of):
    """
    lc = models.DjangoLigneCommandeApprov.objects.filter(product_id="C201906240")
    """
    queryset = models.ItemCartProduct.objects.filter(product_id=of)

    ll = queryset.values_list('product_id', 'article').distinct()
    df = read_frame(ll, fieldnames=['product_id', 'quantite_panier', 'quantite_prevue'])
    # on sum la qte Panier
    dfg = df.groupby('product_id').sum()
    aa = dfg.aggregate('quantite_panier')
    #---
    row = dict(aa.items())
    somme_qte_panier = int(row[queryset.first().product_id])
    return somme_qte_panier

def listp_item_incart(request):
    context = dict()
    context['item_list'] =  models.Item.objects.all()
    #  messages.add_message(self.request, messages.INFO, 'in get()= %s' % self.cartdb)
    return render(request, "cart.html", context)

