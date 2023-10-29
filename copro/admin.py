import os
from django.contrib import admin
from copro import models as pro_models
from accounts import models as acc_models
from django.conf import settings
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.utils import quote
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join



# Register your models here.
class BaseReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True 

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            # if request.user.get_username() == 'admin':
            if request.user.is_superuser :
                return True
            else :
                return False
        return False

class PieceInline(admin.StackedInline):
    model = pro_models.Piece
    extra = 1
    
    def save_form(self, request, obj, form, change):
        # save residance
        obj.name = obj.file.name
        print("Toto ....... !")
        obj.save()
        


class DocumentAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.Residence._meta.get_fields()]

class EtudeAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.Etude._meta.get_fields()]
    list_display  = ('title', 'description',  'created_at', 'get_author', 'get_documents', )
    #list_select_related = ('author',  )
    search_fields = ['title',]
    
    def get_author(self, obj):
        return obj.created_by.username

    def get_documents(self, obj):
        return obj.documents.all().first()
    
class PjointeInline(admin.StackedInline):
    model = pro_models.Pjointe
    extra = 1
class LigneDeCandidatureAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    inlines = [PjointeInline]

    list_display  = [f.name for f in pro_models.LigneDeCandidature._meta.get_fields()]
    list_filter = ('author', 'created_at', )
    #raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'
    search_fields = ['societe',]
    exclude = ["title", ]
    #fields = [("societe", "contacte"), "comment"]
    list_display = ["upper_societe", "contacte", "role", "telephone", "adresse", "site_web", "status", "get_documents",  ]

    @admin.display(empty_value="???")
    def get_author(self, obj):
        return obj.author.username
    
    @admin.display(description="Societe")
    def upper_societe(self, obj):
        return f"{obj.societe}".upper()

    def get_comment(self, obj):
        return obj.comment[:30]
    
    @admin.display(description="Pieces jointe")
    def get_documents(self, obj):
        # return obj.pieces.all().first()
        pieces = pro_models.Pjointe.objects.filter(candidature=obj.pk)
        # image_path =  os.path.join(settings.BASE_DIR, 'media', 'upload')
        pj = '<br>'.join(["--<a href='/media/{}'>{}</a>"
                .format(ff.piece.name, os.path.basename(ff.piece.name))
                for ff in pieces])
        # return  mark_safe("<br> *** <a href='/media/{}'>toto</a> ".format(pieces[0].piece.name)) 
        return mark_safe(pj)
        
    get_documents.allow_tags = True
    get_documents.short_description = "doc id"

    
    def get_changeform_initial_data(self, request):
        return {
            'author': 1, 
            'etude': 1, 
            }

class ResidenceAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display  = ['photo', 'name', 'adresse', 'get_documents' ]
    list_display_links  = ('photo', 'name', 'get_documents', )
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

    def photo(self, obj):
        return mark_safe("<img src='/media/{}'  alt='la photo'/>".format(
            obj.image,
        )) 
    
    def save_model(self, request, obj, form, change):
        # save residance
        obj.save()
        # save pieces jointes
        for afile in request.FILES.getlist('photos_multiple'):
            print("photo name {}".format(afile.name))
            obj.photos.create(image=afile)

class PrestationServiceAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.PrestationService._meta.get_fields()]

class AccountsAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in acc_models.CustomUser._meta.get_fields()]
    list_display.remove("groups")
    list_display.remove("user_permissions")
    

# registre
#admin.site.register(pro_models.Residence, ResidenceAdmin)
admin.site.register(pro_models.Residence, ResidenceAdmin)
admin.site.register(pro_models.Etude, EtudeAdmin)
admin.site.register(pro_models.LigneDeCandidature, LigneDeCandidatureAdmin)
admin.site.register(pro_models.PrestationService, PrestationServiceAdmin)
admin.site.register(acc_models.CustomUser, AccountsAdmin)
