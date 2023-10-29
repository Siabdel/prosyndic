from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView
# local 
from copro import models as pmodel

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


class PortailHome(ListView) :
    template_name = "home/home_page.html"
    
    def get_template_names(self) :
        ## template_name = "home/home_material_page.html"
        return "home/home_agency_page.html"
            
            
    
    def get_context_data(self, **kwargs) :
        context =  super(PortailHome, self).get_context_data(**kwargs)
        template_design = pmodel.Params.objects.get(name='TEMPLATE_THEME')
        # assigni context
        context['TEMPLATE_DESIGN']     = template_design.c_value
        context['PROJECT_DIR']  = settings.PROJECT_DIR 
        return context
    