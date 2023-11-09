import os
from django.contrib import admin
from copro import models as pro_models
from accounts import models as acc_models
from django.conf import settings
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.utils import quote
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join, format_html
from markdownx.admin import MarkdownxModelAdmin 

admin.site.site_header = "PROSYNDIC Admin"
admin.site.site_title = "PROSYNDIC Admin Portal"
admin.site.index_title = "Welcome to PROSYNDIC Portal"
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
        
class PieceEtudeInline(admin.StackedInline):
    model = pro_models.PJEtude
    extra = 1
    

class DocumentAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.Residence._meta.get_fields()]

@admin.register(pro_models.Etude)
class EtudeAdmin(admin.ModelAdmin):
    inlines = [PieceEtudeInline]
    list_display  = ('title', 'description', 'type_presta',  'created_at', 'get_author', 'get_documents', )
    #list_select_related = ('author',  )
    search_fields = ['title',]
    fields  = ('title', 'description',)
    
    def get_author(self, obj):
        return obj.created_by.username

    def get_documents_(self, obj):
        return obj.documents.all().first()
    
    @admin.display(description="Pieces jointe")
    def get_documents(self, obj):
        # return obj.pieces.all().first()
        pieces = pro_models.PJEtude.objects.filter(etude=obj.pk)
        # image_path =  os.path.join(settings.BASE_DIR, 'media', 'upload')
        pj = '<br>'.join(["--<a href='/media/{}'>{}</a>"
                .format(ff.piece.name, os.path.basename(ff.piece.name))
                for ff in pieces])
        # return  mark_safe("<br> *** <a href='/media/{}'>toto</a> ".format(pieces[0].piece.name)) 
        return mark_safe(pj)
    
class PjointeInline(admin.StackedInline):
    model = pro_models.Pjointe
    extra = 1

@admin.register(pro_models.LigneDeCandidature)
class LigneDeCandidatureAdmin(BaseReadOnlyAdminMixin, MarkdownxModelAdmin):
    inlines = [PjointeInline]

    list_display  = [f.name for f in pro_models.LigneDeCandidature._meta.get_fields()]
    list_filter = ('author', 'created_at', )
    #raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'
    search_fields = ['societe',]
    exclude = ["title", ]
    #fields = [("societe", "contacte"), "comment"]
    list_display = ["upper_societe", "contacte", "role", "telephone", "site_web", "status", "notation", "get_documents",  ]
    list_filter  = ('status', 'etude',  )
    list_filter = ('societe', 'offre_recu',  )

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
    
    def thumbnail(self, obj):
        width, height = 100, 200
        html = '<img src="/{url}" width="{width}" height={height} />'
        return format_html( html.format(url=obj.cover.url, width=width, height=height)
        )
        
    get_documents.allow_tags = True
    get_documents.short_description = "doc id"
    # sort comumn
    upper_societe.admin_order_field = "societe"
    
    def get_changeform_initial_data(self, request):
        return {
            'author': 1, 
            'etude': 1, 
            }

@admin.register(pro_models.Residence)
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
    list_display = ['name', 'code', 'description']

# @admin.register(acc_models.CustomUser)
class AccountsAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in acc_models.CustomUser._meta.get_fields()]
    list_display.remove("groups")
    list_display.remove("user_permissions")
    

@admin.register(pro_models.Contacte)
class ContacteAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in pro_models.Contacte._meta.get_fields()]
    list_display = list_total
@admin.register(pro_models.Evenement)
class EventAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in pro_models.Evenement._meta.get_fields()]
    list_display = list_total


@admin.register(pro_models.Ticket)
class TicketAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in pro_models.Ticket._meta.get_fields()]
    list_display = list_total
    list_display = ['title', 'description', 'residence', 'status', 'due_date',  ]


# registre
admin.site.register(pro_models.PrestationService, PrestationServiceAdmin)
admin.site.register(pro_models.Category, )
