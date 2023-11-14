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
from django.contrib.contenttypes.admin import GenericStackedInline
from django.utils import timezone
from itertools import chain


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
    

class CandidatInline(admin.StackedInline):
    model=pro_models.LigneDeCandidature
    extra=5
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
    list_display = ["upper_societe", "contacte", "role", "telephone", "email",
                    "remuneration", "budget_global",
                    "reference", "budget_securite", "budget_jardinage",
                    "get_site_web", "notation", "get_documents",  ]
    list_filter  = ('status', 'etude',  )
    list_filter = ('societe', 'offre_recu', 'etude',  )

    @admin.display(empty_value="???")
    def get_author(self, obj):
        return obj.author.username
    
    @admin.display(description="site web")
    def get_site_web(self, obj):
        return mark_safe("<a href='{}' target='_blanc' />{} </a>".format(obj.site_web, obj.site_web))
        
    
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

@admin.register(pro_models.PrestationService)
class PrestationServiceAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pro_models.PrestationService._meta.get_fields()]
    list_display = ['name', 'code', 'description']

 

@admin.register(pro_models.Contacte)
class ContacteAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in pro_models.Contacte._meta.get_fields()]
    list_display = list_total

class PieceJointeInline(admin.StackedInline):
    model = pro_models.PJEvent
    extra = 1
@admin.register(pro_models.Evenement)
class EventAdmin(admin.ModelAdmin) :
    inlines = [PieceJointeInline]
    list_total  = [ f.name for f in pro_models.Evenement._meta.get_fields()]
    list_display = ["title", "description", "start", "delai_start", "end", "closed", "get_documents",  ]
    fields = ['title', 'start', 'end',]
    #list_editable = fields
    exclude = ('category', )
    
    def delai_start(self, obj):
        aujourdhui = timezone.now()
        nb_jours = obj.start - aujourdhui
        if nb_jours.days > 0:
            return "reste {} jours".format((obj.start - aujourdhui).days)
        else :
            return ""
        
    @admin.display(description="Pieces jointe")
    def get_documents(self, obj):
        # return obj.pieces.all().first()
        pieces = pro_models.PJEvent.objects.filter(event=obj.pk)
        # image_path =  os.path.join(settings.BASE_DIR, 'media', 'upload')
        pj = '<br>'.join(["--<a href='/media/{}'>{}</a>"
                .format(ff.piece.name, os.path.basename(ff.piece.name))
                for ff in pieces])
        # return  mark_safe("<br> *** <a href='/media/{}'>toto</a> ".format(pieces[0].piece.name)) 
        return mark_safe(pj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)
        #form.base_fields['Category'].queryset = pro_models.Category.objects.filter(title__iexact='economie')
        return form


@admin.register(pro_models.Ticket)
class TicketAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in pro_models.Ticket._meta.get_fields()]
    list_display = list_total
    list_display = ['title', 'description', 'residence', 'status', 'due_date',  ]

# base de données de documents 
@admin.register(pro_models.Document)
class BaseDocuments(admin.ModelAdmin):
    list_display = ['do_title', 'get_documents',  ]
    search_fields  = ["get_documents", ]

    def get_documents(self, obj):
        # return obj.pieces.all().first()
        pieces1 = pro_models.PJEtude.objects.all()
        pieces2 = pro_models.PJEvent.objects.all()
        pieces3 = pro_models.Pjointe.objects.all()
        all_pieces = list(chain(pieces1, pieces2, pieces3))
        # image_path =  os.path.join(settings.BASE_DIR, 'media', 'upload')
        pj = '<br>'.join(["--<a href='/media/{}'>{}</a>"
                .format(ff.piece.name, os.path.basename(ff.piece.name))
                for ff in all_pieces])
        return mark_safe(pj)
    
    
# registre
admin.site.register(pro_models.Category, )
