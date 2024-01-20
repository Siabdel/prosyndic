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
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from simulator import forms 
from django.contrib import messages
from cartcom.cart import Cart
from cartcom import models as cart_models
from .models import Rubrique, SousRubrique, ChargesFonctionnement
from simulator.serializers import RubriqueSerializer, SousRubriqueSerializer, ChargesFonctionnementSerializer
from rest_framework import generics

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
class ListItemCartView(ListView, Cart, JsonResponseMixin):
    """
    Gestionnaire OFS
    """
    template_name="of_list.html"
    object_list = None
    # form_class = forms.SearchForm
    model = cart_models.ItemArticle
    # paginate_by = 10  # if pagination is desired


    def get_context_data(self,  **kwargs):
        context = super(ListItemCartView, self).get_context_data(**kwargs)
        # init panier Cart
        Cart.__init__(self, self.request)

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



class RubriqueListCreateView(generics.ListCreateAPIView):
    queryset = Rubrique.objects.all()
    serializer_class = RubriqueSerializer

class SousRubriqueListCreateView(generics.ListCreateAPIView):
    queryset = SousRubrique.objects.all()
    serializer_class = SousRubriqueSerializer

class ChargesFonctionnementListCreateView(generics.ListCreateAPIView):
    queryset = ChargesFonctionnement.objects.all()
    serializer_class = ChargesFonctionnementSerializer
