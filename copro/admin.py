import os
from django.contrib import admin
from copro import models as pro_models
from django.conf import settings
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.utils import quote
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join



# Register your models here.


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
    exclude = ["title", ]
    #fields = [("societe", "contacte"), "comment"]
    list_display = ["upper_societe",  "contacte", "role", "telephone", "status", "get_documents",  ]

    @admin.display(empty_value="???")
    def get_author(self, obj):
        return obj.author.username
    
    @admin.display(description="Societe")
    def upper_societe(self, obj):
        return f"{obj.societe}".upper()

    def get_comment(self, obj):
        return obj.comment[:30]
    
    def get_documents(self, obj):
        return obj.documents.all()
    
    def get_changeform_initial_data(self, request):
        return {
            'author': 1, 
            'etude': 1, 
            }

   

class PieceInline(admin.StackedInline):
    model = pro_models.Piece
    extra = 1
    
    def save_form(self, request, obj, form, change):
        # save residance
        obj.name = obj.file.name
        print("Toto ....... !")
        obj.save()
        

class ResidenceAdmin(admin.ModelAdmin):
    list_display  = ['name', 'adresse', 'get_documents' ]
    list_display_links  = ('name', 'get_documents', )
    inlines = [PieceInline]

    def get_documents(self, obj):
        # return obj.pieces.all().first()
        pieces = pro_models.Piece.objects.filter(residence=obj.pk)
        # image_path =  os.path.join(settings.BASE_DIR, 'media', 'upload')
        pj = '<br>'.join(["--<a href='/media/{}'>{}</a>"
                .format(ff.piece.name, os.path.basename(ff.piece.name))
                for ff in pieces])
        # return  mark_safe("<br> *** <a href='/media/{}'>toto</a> ".format(pieces[0].piece.name)) 
        return mark_safe(pj)
        
    get_documents.allow_tags = True
    get_documents.short_description = "doc id"

    def save_model(self, request, obj, form, change):
        # save residance
        raise Exception 
        obj.save()
        # save pieces jointes
        for afile in request.FILES.getlist('photos_multiple'):
            print("photo name {}".format(afile.name))
            obj.photos.create(image=afile)

# registre
#admin.site.register(pro_models.Residence, ResidenceAdmin)
admin.site.register(pro_models.Residence, ResidenceAdmin)
admin.site.register(pro_models.Etude, EtudeAdmin)
admin.site.register(pro_models.LigneDeCandidature, LigneDeCandidatureAdmin)