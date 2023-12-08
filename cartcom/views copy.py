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
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
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
from .cart import Cart, create_cart_in_database
from .cart import create_item_in_database
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from cartcom import forms
from . import models
import numpy as np
from django_pandas.io import read_frame
import pandas as pd
from . import views as of_views

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
class ListOfsView(ListView, FormView, Cart):
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
                if not models.DjangoLigneCommandeApprov.filter(code_of=of.code_of).exists():
                    messages.add_message(self.request, messages.INFO, 'Of completed DA=%s' % of.code_of)
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
        all_columns = ['demande_appro', 'code_of', 'article', 'commande',
                       'machine', 'quantite_commandee', 'quantite_produit', 'selected']

        lignes_da = new_da_simu.mes_lignes.all()
        #.values_list( 'demande_appro', 'code_of', 'article', 'commande', 'machine', 'quantite_commandee', 'quantite_produit', 'selected' )
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

        code_of = kwargs.get('code_of')
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
# --- Gestion des Demande approv. confirmées
# -----------------------------------------
@method_decorator(login_required, 'dispatch')
class HomeDaOf(ListView, FormView):
    """
    """
    success_url = "/da/home/"

    template_name = "list_of.html"
    model = models.Item
    #paginate_by = 10  # if pagination is desired
    form_class = forms.SearchMachineForm
    object_list = None

    def get(self,request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['semaine_of'] = kwargs.get('semaine_of')
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        # 1- on cahrge le context
        # messages.add_message(self.request, messages.INFO, 'HomeDaOf: PROJECT_PATH =%s' %  BASE_DIR)
        context = super(HomeDaOf, self).get_context_data(**kwargs)
        semaine_aujourdhui = datetime.datetime.isocalendar(datetime.datetime.now())[1]
        annee_actuelle  = datetime.datetime.now().strftime("%Y")[-2:]

        # 2- on charge le formulaire avec request.POST
        if self.request.method == 'POST' :
            form = forms.SearchMachineForm(self.request.POST)
            la_semaine = self.request.POST['semaine']
            annee_saisie = self.request.POST['annee']
            machine_choisie = self.request.POST['machines']
            machine_choisie = models.DjangoMachine.objects.get(codemach=machine_choisie)
            #iquery = LiveDataFeed.objects.values_list('unit_id', flat=True).distinct()
            form.fields['semaine'].initial = la_semaine
            try :
                nom_atelier = planif_models.DjangoLieuProd.objects.get(clieupro=machine_choisie.atelier)
            except Exception as err:
                nom_atelier = machine_choisie
                messages.add_message(self.request, messages.INFO, 'pas atelier trouve en base =%s' % machine_choisie)

            context['machine_choisie'] = nom_atelier

        else:
            form = forms.SearchMachineForm()
            # 3- on inialise form par val machines et semaine
            if 'semaine_of' in context.keys() and 'annee' in context.keys():
                la_semaine= context.get('semaine_of')
                annee_saisie = context.get('annee')[-2:]
            else:
                la_semaine = semaine_aujourdhui
                annee_saisie = annee_actuelle


        # on charge les machines de la listbox
        #messages.add_message(self.request, messages.INFO, 'semaine=%s et annee=%s saisie' % (la_semaine, annee_saisie))
        machines_de_semaine =  planif_models.DjangoOf.objects.filter(
            semaine=la_semaine ,
            annee=annee_saisie ,
            statut__in=['P', 'D'])\
            .distinct().order_by('machine_travail_id__nommach') \
            .values_list('machine_travail_id__codemach', 'machine_travail_id__nommach', flat=False)

        # on charge machine dans form
        machines_de_semaine = [(machine_travail_id__codemach, machine_travail_id__nommach)
                    for (machine_travail_id__codemach, machine_travail_id__nommach)
                    in machines_de_semaine.iterator()]


        form.fields['machines'].choices = machines_de_semaine
        form.fields['semaine'].initial = semaine_aujourdhui
        form.fields['annee'].initial =  annee_saisie

        # 4- on met a jour le context avec autre ariables
        context['annee_actuelle'] = annee_actuelle
        context['annee_saisie'] =  annee_saisie
        context['semaine_of'] = la_semaine
        context['semaine_actuelle'] = semaine_aujourdhui
        context['form'] = form
        context['object_list'] = self.get_queryset(form)

        img_choice = random.choice(range(10))
        context['range'] = img_choice
        context['semaines_avenir'] = [ sem for sem in range(semaine_aujourdhui, 53, 1)]
        return context


    def post(self, request, **kwargs):
        """
        on traite le formulaire valide pour charger les valeurs postées dans kwargs
        """
        form = self.get_form()

        if form.is_valid():
            # messages.error(request, u"semaine saisie %s" %  str(msg))
            #messages.add_message(self.request, messages.INFO, 'form valide =%s' %  form.cleaned_data)
            # on recupere les data user du choix et updater kwargs
            kwargs.update({
                'semaine': form.cleaned_data['semaine'],
                'machines': form.cleaned_data['machines'],
                'jours_semaine': form.cleaned_data['jours_semaine'],
                #'annee': form.cleaned_data['annee'],

                           })
            #
            # return self.render_to_response(self.get_context_data(form=form))
            return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def get_queryset(self, form):
        kwargs = self.get_form_kwargs()
        v_machine = None
        # 1- on recuprer les data de l'utilisateur
        if self.request.method == 'POST':
            v_semaine = self.request.POST.get('semaine')
            v_annee = self.request.POST.get('annee')
            # messages.add_message(self.request, messages.INFO, 'semaine=%s et annee=%s saisie' % (v_semaine, v_annee))


            if  form.is_valid():
                # messages.add_message(self.request, messages.INFO, 'form valide %s' % (form.cleaned_data))
                v_machine = form.cleaned_data['machines']

            else:
                messages.add_message(self.request, messages.INFO, 'form en erreurs =%s' % form.errors )
                return self.object_list

            # jours_semaine': [u'3', u'4'],
            v_jour_semaine = kwargs.get('jours_semaine', [])

            # Default
            v_semaine_courante = datetime.datetime.isocalendar( datetime.datetime.now())[1]
            v_annee_courante  = str(datetime.datetime.isocalendar(datetime.datetime.now())[0])[-2:]
            v_machine_courante  = 'INCONNUE'

            # 2- composer la requete
            #v_semaine = '30'
            # if v_machine :
            self.object_list = planif_models.DjangoOf.objects.filter(semaine=v_semaine,
                                                              annee=v_annee,
                                                          machine_travail_id=v_machine,
                                                          statut__in=['P', 'D'])

            # 3- convertir les jours semaine en dates
            # ..jours_semaine': [u'1', u'5'],
            ofs_du_jours = []
            if len(form.cleaned_data['jours_semaine']) > 0 :
                for jour  in  form.cleaned_data['jours_semaine'] :
                    ofs_du_jours = ofs_du_jours + [of.code_of for of in self.object_list.iterator() if of.date_debut_reelle.weekday() == int(jour) - 1]

                # messages.add_message(self.request, messages.INFO, 'count ofs = %s' % (ofs_du_jours ))
                self.object_list = self.object_list.filter(code_of__in = ofs_du_jours)

            # 4/ test si OF est deja concerné par une Cac
            self.object_list= list(self.object_list)
            for index, of in  enumerate(self.object_list):
                if  models.DjangoLigneCommandeApprov.objects.filter(code_of=of.code_of).exists():
                    cac = models.DjangoLigneCommandeApprov.objects.filter(code_of=of.code_of).first()
                    # messages.add_message(self.request, messages.INFO, 'OF est deja concerne par une Cac=%s' % of.code_of)
                    if  is_quantite_prevue_completed(of) :
                        self.object_list[index].comment = "completed"
                    elif get_sum_quantite_panier(of) > 0 and get_sum_quantite_panier(of) < cac.quantite_pprevue :
                        self.object_list[index].comment = "partialed"
                        self.object_list[index].quantite_prevue = self.object_list[index].quantite_prevue - cac.quantite_panier

        # retour
        return self.object_list

"""
if not created:
    for attr, value in fields.iteritems():
        setattr(instance, attr, value)
"""
#----------------------------
#--- details nomenclature
#----------------------------
@method_decorator(login_required, 'dispatch')
class CacDetailsView(ListView):
    template_name="details_cac.html"
    # models = models.DjangoLigneCommandeApprov
    object_list = None

    def get(self, args, **kwargs):
        cac_id = kwargs.get('cac_id')
        context = self.get_context_data(**kwargs)

        if cac_id :
            self.queryset = models.DjangoLigneCommandeApprov.objects.filter(demande_appro__pk=cac_id)
            context['cdeappro'] = ofsch_models.DjangoEnteteAppro.get(cac_id=cac_id).cdeappro
        else :
            self.queryset =  context['object_list'] = None

        # return
        context['object_list'] = self.queryset
        return self.render_to_response(context)


#  class Cart List items
@method_decorator(login_required, 'dispatch')
class ListItemCartView(ListView, Cart):
    """
    details des produits nomenclature de DAS
    """
    template_name="details_das.html"
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
        CartDemandeAppro.__init__(self, self.request)
        context['object_list'] = context['item_list'] = self.get_items_cart()

        return context


    def get(self, request, *args, **kwargs):
        # on recupere le contexte
        self.request = request
        # initialisation objet panier
        # on recupere le context
        context = self.get_context_data(**kwargs)
        #-------------------------
        action = kwargs.get('action', 'listitem')
        code_of = kwargs.get('code_of', "")
        quantitee = kwargs.get('quantitee', 0)


        if action == "listitem":
            context = self.get_context_data(**kwargs)
            context['item_list'] = self.get_list_items(context)
            #  messages.add_message(self.request, messages.INFO, 'in get()= %s' % self.cartdb)
            return render(self.request, "cart.html", context)

        elif action == "additem" and code_of:
            # ajout of dans panier
            data = self.add_item_of_incart(code_of, quantitee)

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

        elif action == 'update_entete':
            # 1- recuperation des vars
            v_cac_id = kwargs.get('cac_id')
            url_ext_zope = kwargs.get('url_ext')
            # 2- insert en base entete appro + lignes appro
            if not (planif_models.DjangoEnteteAppro.objects.filter(cac_id = v_cac_id).exists()):
                ## new_entete_appro = self.create_da_gestform(v_cac_id)
                url_ext_zope =  url_ext_zope + "?CODE={}&ZONE=entete-pied".format(new_entete_appro.cdeappro)

            else :
                entete_appro = planif_models.DjangoEnteteAppro.objects.get(cac_id = v_cac_id)
                url_ext_zope =  url_ext_zope + "?CODE={}&ZONE=entete-pied".format(entete_appro.cdeappro)

            # redirect
            return redirect(url_ext_zope)


        return self.render_to_response(context)
        #return self.get(args, **kwargs)


  
    # ---------------
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
            item_list = models.Item.objects.filter(cart=self.cartdb)
            # messages.add_message(self.request, messages.INFO, 'je vais dans le panier')

        except Exception as err:
            messages.add_message(self.request, messages.INFO,
                                 'Erreur list panier = %s ' % str(err))
        return item_list

    # ajout de of dans le panier
    def add_item_of_incart(self, code_of, quantitee=0):
        resp = {}
        # messages.add_message(self.request, messages.INFO, 'code of =%s quantitee= %s' % (code_of, self.request.session.get('CART_ID') ))

        try:
            of = planif_models.DjangoOf.objects.get(code_of=code_of)
            if not self.is_product_exist_incart(of):
                # on ajoute dans panier
                self.add(of, 1, quantitee)
                resp['status'] = "OK of ajouter dans panier = %s  " % (code_of)

            else:
                messages.add_message(self.request, messages.INFO, '%s  Article existe deja ! code of=' % code_of)
                resp['status'] = '%s  Article existe deja ! code of=' % code_of

        except Exception as err:
            messages.add_message(self.request, messages.INFO, 'Erreur add of err = %s ' %  err.message)
            resp['status'] = "KO error=%s  " % (str(err))

        return resp

    def del_item_incart(self, item_id):
        try :
            ii = models.Item.objects.get(id=item_id)
            ii.delete()
        except Exception as err:
            messages.add_message(self.request, messages.INFO, 'Erreur del_item_incart = %s ' % item_id)
            pass


    def empty_cart(self):
        ii = models.CartOf.objects.get(id=self.cartdb.id)
        ii.delete()

    def simulation_demande_approv(self, context):
        # 0- recuperer les ofs du panier
        propositions = []

        # on recupere les variables context
        code_machine = context.get('code_machine')
        semaine = context.get('semaine')
        annee = context.get('annee')


        # 1- creation une demande appro simulation
        """
        si une aucune DA non valider n'existe pour cette utilisateur
        on creer une nouvelle DA
        """
        # if not models.DemandeApproSimulee.objects.filter(created_by=self.request.user, statut=1).exists():
        if code_machine and semaine and annee :
            # creation new entete appro
            try :
                machine = models.DjangoMachine.objects.get(codemach=code_machine)
                # messages.add_message(self.request, messages.INFO, 'error : machine= %s' % (code_machine))

                atelier = planif_models.DjangoLieuProd.objects.get(clieupro=machine.atelier)
                v_atelier = atelier.llieupro

            except Exception as err :
                    machine   = None
                    v_atelier = None
                    messages.add_message(self.request, messages.INFO, 'error : %s' % (str(err) ))



            new_da_simu = models.DemandeApproSimulee.objects.create(statut=1,
                                                     created_by=self.request.user,
                                                     entrepot='SCE Lentilly', zone_appro=v_atelier,
                                                     semaine=semaine, annee=annee, machine=machine)
            # save
            new_da_simu.save()
        else:
            # new_da_simu = models.DemandeApproSimulee.objects.filter( statut=1).first()
            messages.add_message(self.request, messages.INFO, 'error paramettre incomplet = %s' % (code_machine))
            return False

        # 2- calculer les DA pour charque of

        # 3- Integrer les ligne de demande appro simule in CartArticleConditionnement
        mes_articles_of = self.cartdb.item_set.all()
        # messages.add_message(self.request, messages.INFO, 'mes_produits simulees= %s' % (mes_articles_of))

        for item in mes_articles_of:
            # messages.add_message(self.request, messages.INFO, 'add ligne DA = %s ' % item.product.code_of )
            self.add_ligne_appro(new_da_simu, item)

        # 4 afficher la proposition
        lignes_da = new_da_simu.mes_lignes.all().order_by("code_of")

        # --------------
        # PANDAS stats
        # -------------
        df = read_frame(lignes_da, fieldnames=['code_of', 'quantite_produit'])

        # 5- grouper par of les produits
        dfg = df.groupby('code_of').count()
        val = list(dfg.values)
        index = list(dfg.index)
        of_count = zip(index, val)

        dfg_count = dfg.items()

        # 6- grouper par of on calcul la somme des quantitée produit
        df_qte_produit = df.groupby(df['code_of']).sum()
        sum_qq = df_qte_produit.quantite_produit

        indice = 0
        for elem in lignes_da:
            for of, counter in of_count:
                if of == elem.code_of:
                    nb = counter[0]
            elem.comment = nb


        #json_data = self.render_json_response(lignes_da)

        return new_da_simu

    # -------------------------------------------------
    # -- copy cart simulé en commande appro confirmée
    # --------------------------------------------------
    def transforme_cart_commande_da(self, old):
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
                    if is_quantite_prevue_completed(new_ligne_cda.code_of) :
                        new_ligne_cda.completed = True
                    elif (get_sum_quantite_panier(new_ligne_cda.code_of) > 0) and (get_sum_quantite_panier(new_ligne_cda.code_of) < cac.quantite_pprevue) :
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
# API Demande approv
#-----------------------

def api_add_item_of_incart(request, code_of):
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
        of = planif_models.DjangoOf.objects.get(code_of=code_of)
        #messages.add_message(request, messages.INFO, 'ajout de of dans le panier.%s' % code_of)
        messages.add_message(request, messages.INFO,  ' mon panier in request= %s ' % str(
            request.session.get('CART_ID')))
        item = create_item_in_database(panier, of)
    except Exception as err:
        messages.add_message(request, messages.INFO,
                             'Erreur dans add_item_of_incart: %s pour code of %s' % (str(err), code_of))

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
        lignes_da = da_encours.mes_lignes.all().order_by("code_of")
        # lignes_da_json =  calcul_demande_appo_cumulee(9 )
        # messages.add_message(request, messages.INFO, 'Erreur dans api_demande_appro_sim %s' % (lignes_da_json))

        # 3 afficher la proposition
        serializers.serialize("json", lignes_da, stream=response)
        #json_data = serializers.serialize('json', lignes_da)
        #---------------
        # return HttpResponse(json.dumps(response_data), content_type="application/json")
        return response


def api_get_machines(request, code_machine, semaine, annee):

        response_data = []
        #machines = models.DjangoMachine.objects.raw('SELECT  codemach as id, nommach   FROM machine')
        #machines = models.DjangoMachine.objects.exclude(nommach = "INCONNU", codemcond = "").exclude(nommach = "", codemcond = "INCONNU")
        # ['A9',  'C5', 'F6', 'C4', 'D1', 'A7', '32', 'D3']
        #machines_of = planif_models.DjangoOf.objects.values('machine_travail').distinct().order_by('machine_travail').filter(machine_travail__in = [  'C4', 'A9'], )
        # on complete a 2 cars avec '0'
        semaine_1 = str(get_delta_week(
            int(annee), int(semaine),  -1)[1]).zfill(2)
        semaine_plus_1 = str(get_delta_week(
            int(annee), int(semaine),  +1)[1]).zfill(2)
        semaine_plus_2 = str(get_delta_week(
            int(annee), int(semaine),  +2)[1]).zfill(2)
        semaine_plus_3 = str(get_delta_week(
            int(annee), int(semaine),  +3)[1]).zfill(2)

        # on charge les ofs de (S-1, S, S+3) pour la vue mensuel
        #ofs_total = ofs_1  | ofs_2

        machines_of = planif_models.DjangoOf.objects.filter(annee=annee,
                                                     machine_travail=code_machine,
                                                     semaine__in=(
                                                         semaine_1, semaine, semaine_plus_1, semaine_plus_2, semaine_plus_3)
                                                     ).distinct().order_by('machine_travail').values('machine_travail')  # ofs de semaine +3

        lesmachines = []
        for elem in machines_of:
            code_machine = elem['machine_travail']
            machine = models.DjangoMachine.objects.get(codemach=code_machine)
            lesmachines.append((code_machine, machine.nommach))

        background_color = '#fff9bf'
        text_color = 'blue'
        for code, nommach in lesmachines:
            ## id: "b", title: "Room B", eventColor: "green"
            response_data.append({
                "color": "f33",
                "backgroundColor": '#fff9bf',
                "eventColor": '#fff9bf',
                "id": code,
                "title": nommach[:20],
                #"eventColor" : "#4f4" ,
            })

        # renoie
        #logger.debug('event !' + str(ofs.first()) )
        return HttpResponse(json.dumps(response_data), content_type="application/json")

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
                code_of=id)
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
    queryset = models.DjangoLigneCommandeApprov.objects.filter(code_of=of.code_of)

    ll = queryset.values_list('code_of', 'article').distinct()
    df = read_frame(ll, fieldnames=['code_of', 'quantite_panier', 'quantite_prevue'])
    # on sum la qte Panier
    dfg = df.groupby('code_of').sum()
    aa = dfg.aggregate('quantite_panier')
    # ---
    row = dict(aa.items())
    somme_qte_panier = int(row[queryset.first().code_of])
    return somme_qte_panier >= queryset.first().quantite_prevue


def get_sum_quantite_panier(of):
    """
    lc = models.DjangoLigneCommandeApprov.objects.filter(code_of="C201906240")
    """
    queryset = models.DjangoLigneCommandeApprov.objects.filter(code_of=of)

    ll = queryset.values_list('code_of', 'article').distinct()
    df = read_frame(ll, fieldnames=['code_of', 'quantite_panier', 'quantite_prevue'])
    # on sum la qte Panier
    dfg = df.groupby('code_of').sum()
    aa = dfg.aggregate('quantite_panier')
    #---
    row = dict(aa.items())
    somme_qte_panier = int(row[queryset.first().code_of])
    return somme_qte_panier

def listp_item_incart(request):
    context = dict()
    context['item_list'] =  models.Item.objects.all()
    #  messages.add_message(self.request, messages.INFO, 'in get()= %s' % self.cartdb)
    return render(request, "cart.html", context)


class AddCommentDa(FormView):
    """
    fetch(apiURL, {
            method: 'POST',
            credentials: 'include',
            headers: {
              	'X-CSRFToken': cle_csrf,
            },
    """
    template_name = "form_add_message.html"
    form_class = forms.CommentDaForm
    model = models.DjangoCommandeApprov
    success_url = "/da/cac/list/"


    #@ensure_csrf_cookie
    def post(self, request, *args, **kwargs):
        # 1/ on va recperer le commantaire saisi
        form = self.form_class(request.POST)
        data =  json.loads(request.POST.dict().keys()[0])
        # on verifie si le formulaire est valide
        if request.method == 'POST'  :
            # messages.add_message(self.request, messages.INFO, 'form valid() = %s' % data)
            # 2/ on récupere la semaine, annee, et machine saisie par l'utilsateur
            v_comment = data["comment"]
            # 3/ save les elements
            # cac_id = kwargs.get("pk")
            cac_id = data["cac_id"]
            self.object = self.model.objects.filter(pk=cac_id)
            self.object.update(comment=v_comment)

            return HttpResponse("ok update ...")

        elif not form.is_valid() :
            return self.form_invalid(form)

        return render(request, self.template_name, locals())




def crud_demande_appro(request):
    """
    console liste des commande appro
    """
    template = "console/da_crud.html"
    #And render it!
    context = dict()

    # qs = models.DjangoOf.objects.filter(semaine='38', annee='18' ).values_list('code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
    qs = models.DjangoCommandeApprov.objects.all()
    # df = read_frame(qs, fieldnames = ['machine_travail', 'quantite_commandee'])
    columns = [ f.name for f in models.DjangoCommandeApprov._meta.get_fields() ]
    # 'annee', 'comment', 'created', 'created_by', 'created_by_id', 'demande_appro_id', 'entrepot', id, 'lignes_cda', 'machine', machine_id, semaine, statut, zone_appro

    df = read_frame(qs, fieldnames =  ['id', 'created', 'created_by',
                                       'created_by_id', ])
    # entete de colonnes
    # columns = of_views.construct_columns(df.columns)
    #Write the DataFrame to JSON (as easy as can be)
    #json = dfg.to_json(orient='records')  # output just the records (no fieldnames) as a collection of tuples
    # output just the records (no fieldnames) as a collection of tuples
    json = df.to_json(orient='records')
    #Proceed to create your context object containing the columns and the data
    context = {
             'data': json,
             'columns': columns
            }
    return render(request, template, context)


def liste_commandes_set():
    from ofschedule import models as ofsch_models
    commandes = set(ofsch_models.DjangoOf.objects.filter(  semaine='26').values_list('date_debut_reelle',
                                                                                     'commande_id',
                                                                                     'quantite_prevue').distinct())
    return commandes
