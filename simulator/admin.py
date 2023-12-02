from django.contrib import admin
from . import models as ss_models

# Register your models here.
class ItemInline(admin.TabularInline):
    model = ss_models.PosteItem
    extra = 8

@admin.register(ss_models.PosteItem)
class PosteItemAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in ss_models.PosteItem._meta.get_fields()]
    
@admin.register(ss_models.Devis)
class DevisAdmin(admin.ModelAdmin):
   ## inlines = [ItemInline]

    list_display  = [f.name for f in ss_models.Devis._meta.get_fields()]
    #list_display.remove('item')
    