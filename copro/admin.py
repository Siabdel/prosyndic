from django.contrib import admin
from copro import models as pro_models

# Register your models here.

class ResidenceAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.Residence._meta.get_fields()]
  
class DocumentAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.Residence._meta.get_fields()]

class EtudeAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.Etude._meta.get_fields()]
    list_display  = ('title', 'description',  'created_at', 'get_author', 'get_documents', )
    #list_select_related = ('author',  )
    search_fields = ['title',]
    
    def get_author(self, obj):
        return obj.author.username

    def get_documents(self, obj):
        return obj.documents.all().first()
    
class LigneDeCandidatureAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.LigneDeCandidature._meta.get_fields()]
    list_filter = ('author', 'created_at', )
    #raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'
    search_fields = ['societe',]
    exclude = ["title", "author"]
    #fields = [("societe", "contacte"), "comment"]
    list_display = ["upper_societe", "status", "contacte", "comment"]

    @admin.display(empty_value="???")
    def get_author(self, obj):
        return obj.author.username
    
    @admin.display(description="Societe")
    def upper_societe(self, obj):
        return f"{obj.societe}".upper()

    
    def get_documents(self, obj):
        return obj.documents.all().first()
    
    def get_changeform_initial_data(self, request):
        return {
            'author': 1, 
            'etude': 1, 
            }

   

# registre
admin.site.register(pro_models.Residence, ResidenceAdmin)
admin.site.register(pro_models.Etude, EtudeAdmin)
admin.site.register(pro_models.LigneDeCandidature, LigneDeCandidatureAdmin)