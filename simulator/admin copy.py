from django.db import models
from django.contrib import admin
from simulator import models as ss_models
from cartcom import models as cart_models
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms



 
# For Creating test data
def create_item_raw():
    item_raw = cart_models.ItemRaw()
    item_raw.raw_message = "test"
    item_raw.save()

    user_event = cart_models.ItemArticle()
    user_event.content_object = item_raw
    user_event.save()

class ItemRawInline(admin.TabularInline):
    model = cart_models.ItemRaw
    extra = 3
# Register your models here.
@admin.register(ss_models.Devis)
class DevisAdmin(admin.ModelAdmin) :
    # inlines = [ItemRawInline]
    list_total  = [ f.name for f in ss_models.Devis._meta.get_fields()]
    list_display = list_total
    
    
class StudentSolutionInlineAdmin(GenericTabularInline):
    model = StudentSolution
    extra = 1

class StudentSolutionAdminForm(forms.ModelForm):
    class Meta:
        model = StudentSolution
        fields = '__all__'  # Keep all fields 

@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    form = StudentSolutionAdminForm
    inlines = [StudentSolutionInlineAdmin]