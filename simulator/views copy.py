# -*- coding:UTF-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import logging
import pytz
import json
import datetime
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.generic.edit import UpdateView, CreateView, DeleteView, ModelFormMixin, ProcessFormView, FormView, FormMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from cartcom.cart import CartDemandeAppro
from simulator import models as cart_models
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from simulator import forms 
from django.contrib import messages

# Create your views here.

def index(request):
    return HttpResponse("Simulator Ok")

class JsonResponseMixin(object):
    """
    Return json
    """
    def render_to_json(self, queryset):
        # queryset  serialise
        data = serializers.serialize('json', queryset)

        json_data = json.loads( data)
        # json_data = json.dumps( data)

        # data_light = [ (elem['pk'], elem['fields']) for elem in json_data ]
        data_light = [ ]
        for elem in json_data:
            elem['fields']['pk'] = elem['pk']
            data_light.append(elem['fields'])

        data_fin = json.dumps(data_light)
        return HttpResponse(data_fin ,  content_type='application/json')

    def export_as_json(self, ct, ids):
        queryset = ofmodels.DjangoOf.objects.filter(id__in=ids.split(","))
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response

    def export_as_cvs(self, ct, ids):
        queryset = ofmodels.DjangoOf.objects.filter(id__in=ids.split(","))
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        # response['Content-Disposition'] = 'attachment; filename="%s"'% os.path.join('export', 'export_of.csv')
        writer = csv.writer(response)
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.code_of),
                smart_str(obj.client),
            ])
        return response

#  class Cart List items
@method_decorator(login_required, 'dispatch')
class ListOfView(ListView, CartDemandeAppro, JsonResponseMixin):
    """
    Gestionnaire OFS
    """
    template_name="of_list.html"
    object_list = None
    # form_class = forms.SearchForm
    model = ofmodels.DjangoOf
    # paginate_by = 10  # if pagination is desired


    def get_context_data(self,  **kwargs):
        context = super(ListOfView, self).get_context_data(**kwargs)
        # init panier Cart
        CartDemandeAppro.__init__(self, self.request)

        return context

    def get(self, request, *args, **kwargs):
        # on recupere le contexte
        context = self.get_context_data(**kwargs)
        #-------------------------
        action = kwargs.get('action', 'list')

        if action == "list":
            context = self.get_context_data(**kwargs)
            context['object_list'] = self.get_queryset()
            #  messages.add_message(self.request, messages.INFO, 'in get()= %s' % self.cartdb)
            return render(self.request, "of_list.html", context)

        elif action == "apilist":
            context = self.get_context_data(**kwargs)
            queryset = self.model.objects.all()
            queryset = queryset.filter(semaine='28')
            # paginator = Paginator(queryset, 25) # Show 25 contacts per page
            return self.render_to_json(queryset)

        return self.render_to_response(context)


#  class Cart List items
@method_decorator(login_required, 'dispatch')
class ListItemCartView(ListView, CartDemandeAppro):
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
            # data = self.ajax_cart_validate_da(dem_appro_pk)
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


    def create_da_gestform(self, cac_id):
        """
        creation demande appro Gestform a partir d'1 commande appro pulsar
        """
        # 0- charger models.DjangoLigneCommandeApprov.objects.get(pk=cac_id)
        try:
            commande_appro = models.DjangoCommandeApprov.objects.get(pk=cac_id)
        except Exception as err:
            # pas de commande
            messages.add_message(self.request, messages.INFO, 'erreur create_da_gestform = %s' % err.message)
            raise
        # 1-construct code entete appro

        dernier_entete_app = planif_models.DjangoEnteteAppro.objects.all().order_by('cdeappro').last()
        buffer = dernier_entete_app.cdeappro[4:8]
        fin_code =  str(int(buffer) + 1)
        fin_code =  fin_code.zfill(4)

        # new code
        nouv_code = 'AP'+str(datetime.datetime.now())[2:4]
        nouv_code = nouv_code + fin_code
        # 2-creation de enregistgrement entete appro
        new_da = planif_models.DjangoEnteteAppro.objects.create(
                cdeappro=nouv_code , #cac=cac_id ,
                datecdea=datetime.datetime.now(),
                pour_qui='SERVICE APPROVISIONNEMENT',
                delapart=self.request.user.username,
                cac_id = commande_appro.pk )


        # 3- creation ligne appro
        try:
            new_da.save()
            messages.add_message(self.request, messages.INFO, 'create demande appro gestform = %s' % new_da.cdeappro)

        except Exception as err:
            messages.add_message(self.request, messages.INFO,
                    'Erreur save DjangoEnteteAppro  = %s' % err.message)
            # nouvelle DA supprimer
            raise

        ligne = 10
        # Creation de l'Entete demande appro
        # [{'article': (u'6328', u'ETIQUETTE INFO. 70 X 37MM N\xb0 CONTROLE'), 'nb_of': 13, 'quantite_tot': 643.19 },
        lignes_da_groupees = calcul_demande_appo_cumulee(cac_id)
        # messages.add_message(self.request, messages.INFO, 'calcul_demande_appo_cumulee = %s' % lignes_da_groupees)

        #
        # for ligne_cac in comamnde_appro.lignes_cda.all():
        for ligne_cac in lignes_da_groupees:
            """
            new_da = models.DjangoLigAppro.objects.create
            """
            # via sql
            username = self.request.user.username
            code_article, libelle = ligne_cac['article']
            # quantite_produit = ligne_cac.quantite_produit * (1 + ligne_cac.taux_perte_mp /100)
            quantite_produit = ligne_cac['quantite_tot']

            sql = """
                INSERT INTO ligappro( cdeappro, lignappr, codeprod,
                qteappro , qteprepa , qteappor, date_modif , heure_modif  , login_modif)
                VALUES(
                 '{}', {}, '{}', {}, {}, {}, '{}', '{}', '{}' )
                """.format(new_da.cdeappro, ligne, code_article,
                           quantite_produit , 0, 0,
                           datetime.datetime.now().strftime("%Y-%m-%d"),
                           datetime.datetime.now().strftime("%H:%M"),
                           self.request.user.username)

            # messages.add_message(self.request, messages.INFO, 'sql  = %s' % sql)
            #  INSERT INTO ligappro( cdeappro , lignappr , codeprod , qteappro , qteprepa , qteappor, date_modif , heure_modif , login_modif, )
            #  VALUES( 289, 12, 1864, 41, 0, 0, '2019-06-20', '10:00', 'abdel' )
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql)
                except Exception as err:
                    # suppresiion entete nouvellement creer
                    sql = " delete from entappro where  cdeappro='{}'".format(new_da.cdeappro)
                    cursor.execute(sql)
                    # messages.add_message(self.request, messages.INFO, 'Error INSERT INTO ligappro  = %s' %  err )
                    raise(err)

            # incremente ligne
            ligne = ligne + 10
        #
        return new_da

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


    # ajout de creation de ligne appro

    def add_ligne_appro(self, demande_appro_courante, item):
        """
        Integrer les ligne de demande appro simule in CartArticleConditionnement
        """
        # 1- on charge of
        try :
            of = planif_models.DjangoOf.objects.get(code_of=item.product.code_of)
            of_quantite_prevue = long(math.ceil(item.quantity))
            of.quantite_prevue =  item.quantity

        except Exception as err :
            messages.add_message(self.request, messages.INFO, "erreur %s ligne approv produit=%s "  % (err.message, item.product))
            return False

        # 2- on calcul la nomencalture des articles suivant les quantite_prevue
        simulation = self.calcul_demande_appo(of)


        # 3- on creer une ligne appro
        for propos in simulation.proposition :
                # chercher pour la meme commande si dans les ligne de commande appro das il ya on de deja coché
                commande_appro = None
                taux_mp = 0
                deja_completed = False
                deja_coches = False

                if models.DjangoLigneCommandeApprov.objects .filter(code_of=of.code_of,
                                                                    commande=of.commande_id,
                                                                    article=propos.produit.codeprod).exists() :

                    """
                    une ligne de cac existe - updater quantite restante si  flag completed == False ## Abandonnée !!
                    """
                    deja_coches = True


                # messages.add_message(self.request, messages.INFO, 'of quantite_prevue=%s ' % (propos.quantite))
                # save en base de ligne appro:
                # calcul du taux de perte mp

                if propos.produit.cperte_mp and propos.produit.cperte_mp > 0:
                    # calcul du taux de perte mp= %s ' % (propos.produit.cperte_mp ) )
                    taux_mp = propos.produit.cperte_mp

                try :
                    # if cac n'existe pas
                    new_ligne_da = models.LigneDemandeApproSimulee(
                                    demande_appro=demande_appro_courante,
                                    item_cart=item,
                                    code_of=of.code_of,
                                    article=propos.produit.codeprod,
                                    nom_article=propos.produit.nomprod[:50],
                                    commande=of.commande,
                                    quantite_prevue=of_quantite_prevue,
                                    quantite_commandee=of.quantite_commandee,
                                    quantite_produit=propos.quantite,
                                    quantite_panier=item.quantity,
                                    selected=False,
                                    completed=deja_completed,
                                    validate=deja_coches,
                                    taux_perte_mp=taux_mp
                                    )

                    # sauvegarde de la ligne d'appro
                    new_ligne_da.save()
                    # messages.add_message(self.request, messages.INFO, 'ligne  %s ' % (propos.ligne) )
                except Exception as err:
                    messages.add_message(self.request, messages.DEBUG,
                    'Erreur lors save LigneDemandeApproSimulee ! %s ' % err )

        return True