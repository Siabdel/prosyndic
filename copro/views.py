# -*- coding:UTF-8 -*-
from __future__ import unicode_literals
import os, sys
import datetime
from django.db.models.query import QuerySet
import pytz
import json
import io
import random
from django.http import HttpResponse
from django.core import serializers
from django.http import Http404
import  rest_framework
from rest_framework.views import APIView
import numpy as np
import pandas as pd
from typing import Any
from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView, TemplateView

from django.shortcuts import get_object_or_404
# local 
from copro import models as pro_models
from accounts import models as acc_models
from itertools import chain
from rest_framework import generics, permissions
from copro import serializers as pro_seriz
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django_pandas.io import read_frame
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import os
from rest_framework import generics
from .models import Document


##from copro.utils import Dict2Obj
# from prosyndic.permissions import IsAuthorOrReadOnly

# Create your views here.

## convert dict to Obj
class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])


def home(request):
    context = {}
    context['BASE_DIR']     = settings.BASE_DIR 
    context['PROJECT_DIR']  = settings.PROJECT_DIR 
    context['DEBUG']         = settings.DEBUG 
    context['ALLOWED_HOSTS'] = settings.ALLOWED_HOSTS
    context['banner_title'] = "Bienvenue à notre  agence web"
    context['banner_content'] = "Bienvenue à notre  agence web"
    
    return render(request, template_name="home/home_agency_page.html")

class Home(TemplateView) :
    template_name = "home/home_agency_page.html"

class PortailHome(TemplateView) :
    template_name = "home/home_services.html"
    
    def get_context_data(self, **kwargs) :
        context =  super(PortailHome, self).get_context_data(**kwargs)
        # assigni context
        context['PROJECT_DIR']  = settings.PROJECT_DIR 
        context['username']  = self.request.user.username
        return context
    
@method_decorator(login_required(login_url="/admin/login"), 'dispatch')
class BaseDonneeDoc(ListView):
    model=pro_models.Document
    template_name = "copro/document_list.html"
    
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        # 
        context['current_user'] = self.request.user
        context['now'] = timezone.now()
        return context
     
    
    def get_queryset(self, **kwargs):
        pieces1 = pro_models.PJEtude.objects.all()
        pieces2 = pro_models.PJEvent.objects.all()
        pieces3 = pro_models.Pjointe.objects.all()
        pieces4 = pro_models.Piece.objects.all()
        self.object_list = list(chain(pieces1, pieces2, pieces3, pieces4))
      
        # self.object_list = pro_models.Document.objects.all().order_by("-created")
        return self.object_list

@method_decorator(login_required(login_url="/admin/login"), 'dispatch')
class CompareViewList(ListView):
   model=pro_models.LigneDeCandidature
   template_name = "copro/compare_list.html"  
   
   def get_queryset(self):
        queryset = pro_models.LigneDeCandidature.objects.all().order_by('societe')
        ## return super().get_queryset()
        return queryset 
    
    
@method_decorator(login_required(login_url="/admin/login"), 'dispatch')
class ComparateurIndicateurstList(ListView):
    template_name = "copro/compare_indicateur_list.html" 
    model = pro_models.LigneDeCandidature
## 
@method_decorator(login_required(login_url="/admin/login"), 'dispatch')
class CandidatPivotList(ListView):
    template_name = "copro/compare_pivot_list.html"  
    model = pro_models.LigneDeCandidature
  
##-----------------------------------------------------------
## API API API 
##-----------------------------------------------------------

class ApiIndicateursList(APIView):
    model = pro_models.LigneDeCandidature
    
    def get(self, request, action='list', format='json'):
        json_data = self.queryset_to_json()
        return JsonResponse(json_data )
            
    def queryset_to_json(self, queryset=None):
        # queryset  serialise
        if not queryset :
            ## queryset = pro_models.LigneDeCandidature.objects.filter(offre_recu=True).order_by('societe')# Convert the QuerySet to a Pandas DataFrame
            queryset = pro_models.LigneDeCandidature.objects.filter(
                societe__in=["VALOR Syndic", "GESTIS", "VERY GESTION"])
            candidat_df = read_frame(queryset)
            # replace NaN to None
            # candidat_df = candidat_df.replace(np.nan, None) 
            # pivote table
            # rename columns
            candidat_df.rename(
                columns={'agent_suivi_local':'agent_suivi_sur_place',
                         'agence_locale':'gestionnaire_a_marrakech'}, inplace=True)
            dpivot = candidat_df.pivot_table(values=
                    [
                    'agent_suivi_sur_place',
                    'gestionnaire_a_marrakech',
                    'effectif_jardinage',
                    'effectif_securite',
                    'effectif_piciniste',
                    'effectif_agent_polyvalent',
                    'effectif_maitre_nageur',
                    'effectif_agent_proprete',
                    'model_prestataires_ext', 'taille_entreprise',
                    'anciennete', 'avis_negatif', 'avis_positif',
                    'visite', 'offre_recu', 'reponse_questionnaire', 'proposition_transition',
                    'propostion_recouverement', 'contrat_engagement',
                    'budget_prev_2024', 'budget_prev_2025', 'process_suivi_prests',
                    'ressource_sur_place',
                    ] ,  columns=['societe'])

            
            # n array 
            dpivot = dpivot.replace(np.nan, None)
            lignes_list = dpivot.values.tolist()
            lignes_json = []
            for ind, index in enumerate(dpivot.index):
                lignes_json.append({'name':index, 'data' : lignes_list[ind]})
                
            #return json.dumps(lignes_json, indent=2)
            all_data = {'index': list(dpivot.index), 
                        'columns': list(dpivot.columns), 
                        'data' : lignes_json }
            return all_data
                                              
                      
##
class ApiCandidatPivotList(APIView):
    model = pro_models.LigneDeCandidature
    
    
    def get(self, request, action='list', format='json'):
        ## return self.get_queryset()
        json_data = self.queryset_to_json()
        # return JsonResponse(json_data, status=200, safe=False)
        return JsonResponse(json_data )
           
    
        
    
    def queryset_to_json(self, queryset=None):
        # queryset  serialise
        if not queryset :
            # queryset = pro_models.LigneDeCandidature.objects.filter(offre_recu=True).order_by('societe')# Convert the QuerySet to a Pandas DataFrame
            queryset = pro_models.LigneDeCandidature.objects.filter(societe__in=["VALOR Syndic", "THAIS", "GESTIS", "VERY GESTION"])

            # Convert the QuerySet to a Pandas DataFrame
            candidat_df = read_frame(queryset)
            # replace NaN to None
            # candidat_df = candidat_df.replace(np.nan, None) 
            # candidat_df = candidat_df.astype(object).where(pd.notnull(candidat_df),None)
            # add column cout moyen mensuel  charge syndic 
            bgobal = candidat_df["budget_global"]
            cout_moyen_mensuel = [bg/312 for bg in bgobal]
            candidat_df.insert(2, "aa_cout_moyen_mensuel", cout_moyen_mensuel, True)
            # ecart par rapport budget global 
            thais_q = pro_models.LigneDeCandidature.objects.filter(societe__contains="Thais").first()
            ecart_budget_global = [round(((bg - thais_q.budget_global )/thais_q.budget_global)*100, 2)  for bg in bgobal]
            # inser column ecart 
            candidat_df.insert(3, "ab_ecart_budget_global", ecart_budget_global, True)
            # total des intervenenant dans la copro
            effectif = [(elem.effectif_jardinage + elem.effectif_securite +
                        elem.effectif_piciniste + elem.effectif_agent_polyvalent +
                        elem.effectif_maitre_nageur + elem.effectif_agent_proprete)  for elem in queryset
                        ]
            
            candidat_df.insert(4, "ac_total_intervenant", effectif, True)
            # Remuneration 
            remuneration = candidat_df["remuneration"]
            candidat_df.insert(5, "ad_remuneration", remuneration, True)
            # Remuneration par appart
            remuneration_appart = [(honoraire/312)/12 for honoraire in remuneration]
            candidat_df.insert(6, "ada_remuner_appart", remuneration_appart, True)
            
            # ecart_remuneration
            ecart_remuneration = [round(((honoraire - thais_q.remuneration)/thais_q.remuneration)*100, 2) for honoraire in remuneration ]
            candidat_df.insert(7, "ae_ecart_remuneration", ecart_remuneration, True)
            # provision inverstissement 
            investissements = candidat_df["provision_investissement"]
            candidat_df.insert(8, "af_provision_invest", investissements, True)
            # Budget global
            budget_global = candidat_df["budget_global"]
            candidat_df.insert(9, "aa_budget_global", budget_global, True)
            # cout salaire des intervenant 
            total_intervenant = candidat_df["ac_total_intervenant"]
            cout_salariale_intervenants = [(effectif * 4500)*12 for effectif in total_intervenant]
            candidat_df.insert(10, "aca_cout_intervenant", cout_salariale_intervenants, True)
            # rename comumn
            candidat_df.rename(
              columns={
                  'agent_suivi_local':'honoraire_syndic',
                  'ad_remuneration': 'ad_honoraire_syndic', 
                  'ae_ecart_remuneration': 'ae_ecart_honoraire_syndic',
                  'ada_remuner_appart': 'ada_honoraire_syndic_appart',
                  },
                    inplace=True)

             
  
            # pivote table
            dpivot = candidat_df.pivot_table(values=
                                             ['aa_budget_global', 
                                              'aa_cout_moyen_mensuel', 'ab_ecart_budget_global',
                                              'ac_total_intervenant', 'aca_cout_intervenant',
                                              'ad_honoraire_syndic', 
                                              'ae_ecart_honoraire_syndic',
                                              'af_provision_invest',
                                              'ada_honoraire_syndic_appart',
                                              'budget_global', 'budget_securite', 
                                              'budget_jardinage', 'budget_picine', 
                                              'budget_menage', 'budget_maintenance',
                                              'budget_agent_suivi', 'consommation_eau',
                                              'consommation_electricite' ] ,  columns=['societe'])

            
            # n array 
            dpivot = dpivot.replace(np.nan, None)
            lignes_list = dpivot.values.tolist()
            lignes_json = []
            for ind, index in enumerate(dpivot.index):
                lignes_json.append({'name':index, 'data' : lignes_list[ind]})
                
            #return json.dumps(lignes_json, indent=2)
            all_data = {'index': list(dpivot.index), 
                        'columns': list(dpivot.columns), 
                        'data' : lignes_json }
            return all_data
            
            
    #--- 
    def to_json(self):
        queryset = pro_models.LigneDeCandidature.objects.all().order_by('societe')# Convert the QuerySet to a Pandas DataFrame
        # Convert the QuerySet to a Pandas DataFrame
        candidat_df = read_frame(queryset)
        dpivot = candidat_df.pivot_table(values=
                        ['remuneration', 'budget_global', 'budget_securite', 
                        'budget_jardinage', 'budget_picine', 
                        'budget_menage', 'budget_maintenance'
                        ] ,  columns=['societe'])

        data_string = dpivot.to_json()
        ##data_json2 = [elem   for elem in data_json]
        json_data = json.loads( data_string)
        print(type(json_data))
        return [json_data]

    
    
class DocumentApiList(generics.ListCreateAPIView):
    serializer_class = pro_seriz.DocumentApiSerializer 
    pieces1 = pro_models.PJEtude.objects.all()
    pieces2 = pro_models.PJEvent.objects.all()
    pieces3 = pro_models.Pjointe.objects.all()
    pieces4 = pro_models.Piece.objects.all()
    ## docs = pro_models.Document.objects.all()
     
    #queryset = list(chain(pieces1, pieces2, pieces3, pieces4, ))
    queryset = pro_models.Piece.objects.all()


# Residence
class ResidenceApiList(generics.ListCreateAPIView):
    serializer_class = pro_seriz.ResidenceApiSerializer 
    queryset = pro_models.Residence.objects.all().order_by('name')

class ResidenceDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = pro_models.Residence.objects.all().order_by('name')
    serializer_class = pro_seriz.ResidenceApiSerializer 
    
# Incident
class IncidentApiList(generics.ListCreateAPIView):
    serializer_class = pro_seriz.IncidentApiSerializer 
    queryset = pro_models.Ticket.objects.all().order_by('title')

class IncidentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = pro_models.Ticket.objects.all().order_by('title')
    serializer_class = pro_seriz.IncidentApiSerializer 

# Document
class DocumentApiList(generics.ListCreateAPIView):
    serializer_class = pro_seriz.DocumentApiSerializer 
    queryset = pro_models.Document.objects.all().order_by('-id')

class DocumentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = pro_models.Document.objects.all().order_by('-id')
    serializer_class = pro_seriz.DocumentApiSerializer 

# Api sydic 
class SyndicApiList(generics.ListCreateAPIView):
    serializer_class = pro_seriz.CandidatApiSerializer

    def get_queryset(self):
        queryset = pro_models.LigneDeCandidature.objects.filter(status='OP').order_by('societe', '-id')
        return queryset


def render_pdf(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document_path = os.path.join(settings.MEDIA_ROOT, str(document.file))
    with open(document_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
    return response
##
## API 
