from typing import Any
import datetime
from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView, TemplateView
# local 
from copro import models as pro_models
from accounts import models as acc_models
from itertools import chain
from rest_framework import generics, permissions
from copro import serializers as pro_seriz
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator
# from prosyndic.permissions import IsAuthorOrReadOnly

# Create your views here.

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

# Document
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

