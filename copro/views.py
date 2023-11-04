from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView, TemplateView
# local 
from copro import models as pmodel
from accounts import models as acc_models

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
## import data 
import pandas as pd
from copro import models as pro_models

def import_data(request):

    df = pd.read_excel("tmp/Candidats Syndic-2023.xls", )
    df.head(3)

    """
    societe                 contact  ...                  Comment ajouter
    0  Energy Real Estate          Mr Nabil Rafki  ...  - 20 ans d'experience dans la gestion immobili...     YES
    1        Salam Gestion            Mr Mohammed  ...  - Base a Marrakech, gere plusieurs immeubles e...     YES
    2              Gestsyn  Mme Chaimaa Bouaanani  ...  - Equipe jeune et dynamique\n- Dans le domaine...     YES
    3            ViaSyndic      Mr Yassine Alaoui  ...  - Base a Marrakech, dans le domaine depuis 200...     YES
    4            PacoClean  Mr Youness El Gazouir  ...  - Base a Marrakech, gere uniquement une reside...   50/50

    [5 rows x 7 columns]

    ##
    f.name for f in pro_models.LigneDeCandidature._meta.get_fields()
    ['pjointe', 'id', 'title', 'created_at', 'etude', 'societe', 'status', 'notation', 
     'adresse', 'site_web', 'contacte', 'role', 'reference', 'telephone', 'recommande_par',
     'visite', 'candidat', 'offre', 'remuneration', 'budget_global', 'author', 'description', 'comment']
    ## columns = ['societe', 'contact', 'rôle', 'tel', 'recommende', 'Comment',
       'ajouter']

    """ 
    ett = pro_models.Etude.objects.all().first()
    auteur = acc_models.CustomUser.objects.get(pk=1)

    
    for elem in df.values :
        # print(elem)
        for elem in df.values :
            print(elem)
            pro_models.LigneDeCandidature(
            etude=et,
            author=auteur,
            societe=elem[0],
            contacte=elem[1],
            role=elem[2],
            telephone=elem[3],
            recommande_par=elem[4],
            description=elem[5],
            candidat=False,
            ).save()


    list_total  = [ f.name for f in pro_models.Ticket._meta.get_fields()]
    