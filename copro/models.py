import os, json
import datetime
import time
from django.db import models
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.auth.models import User
import django
from django.conf import settings
from django.utils.html import format_html
from django.contrib import admin
from markdownx.models import MarkdownxField
from django.utils import timezone
from django.core import serializers

now = django.utils.timezone.now()

TICKET_URGENCY_CHOICES = (
    ('FAIBLE',  _('pas important pas urgent')), # Jaune
    ('CRITIQUE', _('important et pas Urgent')), # vert

    ('MOYEN',   _('uregnt et pas importance')),   # Orange
    ('URGENT',  _('Urgent et Important')),       # Urgent et important
)

TICKET_DEFAULT_URGENCY = 'MOYEN'

TICKET_TYPE_CHOICES = (
    ('BUG', _('bug')),
    ('TASK', _('task')),
    ('IDEA', _('idea')),
)

TICKET_DEFAULT_TYPE = 'BUG'

TICKET_STATUS_CHOICES = (
    ('NOUVEAU', _('nouveau')),
    ('ENCOURS', _('encours')),
    ('RESOLUE', _('resolue')),
    ('CLOTUREE', _("cloturee")),
    ('ANNULEE', _('annulee')),
    ('ENATTENTE', _('en attente')),
)

TICKET_DEFAULT_STATUS = 'NOUVEAU'
TICKET_DEFAULT_URGENCY = 'MOYEN'

# TICKET_CLOSE_STATUSES = ('INVALID', 'DUPLICATE', 'RESOLVED')
TICKET_CLOSE_STATUSES = ('CLOTUREE', 'ANNULEE', )

class Category(models.Model):
    """Category model.
    """
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)

    def _occurences(self):
        object_list = []
        related_objects = self._meta.get_all_related_many_to_many_objects()
        for related in related_objects:
            if related.opts.installed:
                model = related.model
                for obj in model.objects.select_related().filter(categories__title=self.title):
                    object_list.append(obj)
        return object_list
    occurences = property(_occurences)

    def __str__(self):
        return u'%s' % self.title


# Documents pieces jointes
class DocumentJoint(models.Model):
    title = models.CharField(max_length = 100)
    pj_file = models.FileField(upload_to='upload/', blank=True, null=True)
   
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def create_relation(self, obj):
        self.content_object = obj
        self.save()

    def get_document_or_object(self, obj, distinction=None):
        """
        This function allows you to get pieces for a specific object
        If distinction is set it will filter out any relation that doesnt have
        that distinction.
        
        >>> user = User.objects.get(username='tony')
        >>> try:
  ...     Piece.objects.get_piece_for_object(user)
        ... except Piece.DoesNotExist:
        ...     print("failed")
        ...
        failed
        Now if we add a piece it should return the piece
        >>> piece = Piece(name='My Cal')
        >>> piece.save()
        >>> piece.create_relation(user)
        >>> Piece.objects.get_piece_for_object(user)
        <Piece: My Cal>
        """
        ct = ContentType.objects.get_for_model(obj)
        return ct
    
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [ models.Index(fields=["content_type", "object_id"]), ]
   
class Document(models.Model):
    document        = models.FileField(upload_to='documents/', blank=True, null=True)
    do_title           = models.CharField(max_length=255, blank=True, null=True)
    do_description     = models.TextField( blank=True, null=True)
    file_basename   = models.CharField(max_length=50, blank=True, null=True)
    thumbnail_file  = models.CharField(max_length=50, blank=True, null=True)
    file_type       = models.CharField(max_length=20, blank=True, null=True)
    file_size       = models.BigIntegerField(blank=True, null=True)
    initial_name    = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(auto_created=True, auto_now_add=True, blank=True, )
    active  = models.BooleanField(default=False)
    
    def create_relation(self, obj):
        self.content_object = obj
        self.save()

    def get_document_or_object(self, obj, distinction=None):
        """
        This function allows you to get pieces for a specific object
        If distinction is set it will filter out any relation that doesnt have
        that distinction.
        """ 
        ct = ContentType.objects.get_for_model(obj)
        return ct
      
    def __str__(self):
        return "%s" % (self.do_title)

    def __unicode__(self):
        return "%s" % (self.do_tile)


class GDocument(models.Model):
    document  = models.ForeignKey(Document, null=True, blank=True, verbose_name=_('piece jointe'), on_delete=models.CASCADE)
    created   = models.DateTimeField(auto_created=True, auto_now_add=True, blank=True)
    # Listed below are the mandatory fields for a generic relation
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')


class AbstractEnteteDoc(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_created=True, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    ##documents  = GenericRelation(Document)
    documents   = GenericRelation(GDocument, null=True, blank=True) #  les documents rattachées

    def add_document(self, piecej):
        self.documents.add(piecej, bulk=False)
        return True
    
    def documents_join(self):
        return self.documents.all()

    def __str__(self) -> str:
        return self.title
    
    class Meta :
        abstract = True 

   
class AbstractLigneDoc(models.Model):
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    # Piece jointe
    # documents  = GenericRelation('Document')

    def add_document(self, piecej):
        self.documents.add(piecej, bulk=False)
        return True

    def get_documents_join(self):
        return self.documents.all()

    def __unicode__(self):
        return u'%s' % self.title

    def __str__(self):
        return u'%s' % self.title


    class Meta:
        ordering = ('-created_at',)
        abstract = True
        
class AbstractPieceJointe(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    piece = models.FileField(upload_to="upload/")
    created = models.DateField(auto_now=True, auto_created=True)
    modified = models.DateTimeField(auto_now=True, verbose_name=_('Date Creation'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    @property
    def piece_name(self):
        # data = serializers.serialize('json', self.piece)
        #return json.dumps({})
        piece_name = os.path.splitext(os.path.basename(self.piece.name))[0]
        return os.path.basename(piece_name)
        
    @property
    def piece_path(self):
        piece_path =  os.path.join('/media/', self.piece.name)
        return piece_path
    
    @property
    def init_date_created(self):
        # date en secondes 
        ti_c = os.path.getctime(self.piece.path)
        return time.ctime(ti_c)

        

    def save(self): 
        if self.piece.name : 
            self.name = self.piece.name
        # super save
        super(AbstractPieceJointe, self).save()
        
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return "{}".format(self.name)
    
# Commantaire
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()

    def create_relation(self, obj):
        self.content_object = obj
        self.save()

class Rating(models.Model):
    """_summary_
    Notes et avis : les types de contenu peuvent être utilisés pour créer un système de notes et
    d'avis pour différents types de contenu, comme des produits, des restaurants ou des
    services
    """
    score = models.PositiveIntegerField()
    review = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def create_relation(self, obj):
        self.content_object_1 = obj
        self.save()
class Pjointe(AbstractPieceJointe):
    candidature = models.ForeignKey('LigneDeCandidature', on_delete=models.CASCADE)
  
class Piece(AbstractPieceJointe):
    residence = models.ForeignKey('Residence', on_delete=models.CASCADE)
    
class Residence(models.Model):
    name = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(null=True)
    color_code = models.CharField(max_length=6, default="010101")
    image = models.ImageField(upload_to="upload/", null=True)

    class Meta:
        verbose_name = _('Residence')
        verbose_name_plural = _('Residences')
        ordering = ('name',)
    
    @admin.display
    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            self.color_code,
            self.name,
            self.adresse,
        )
    
    
    def __unicode__(self):
        return u'%s' % self.name
    def __str__(self):
        return u'%s' % self.name
   


class PrestationService(models.Model):
    name = models.CharField(_("Prestation de service") , max_length=50)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return "%s" % (self.name)
#  Etude de Projet 


class PJEtude(AbstractPieceJointe):
    etude = models.ForeignKey('Etude', on_delete=models.CASCADE)

class Etude(AbstractEnteteDoc):
    title = models.CharField(max_length=200)
    type_presta = models.ForeignKey(PrestationService, default=1, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return "%s" % (self.title)
    

class LigneDeCandidature(AbstractLigneDoc):
    class STATUS(models.TextChoices):
        ENCOURS = "OP", _("Encours")
        CLOTURE = "FR", _("Cloturé")
        ABANDONNEE = "AB", _("Abondonné")
        EN_ATTENTE = "EA", _("En attente")
    etude = models.ForeignKey(Etude, on_delete=models.CASCADE)
    societe = models.CharField(max_length=50)
    status = models.CharField(_("Status :"), choices=STATUS.choices,
                              default="1", max_length=30)
    notation = models.IntegerField(blank=True, null=True)
    adresse = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField( blank=True, null=True)
    site_web = models.URLField(blank=True, null=True)
    contacte = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    reference = models.CharField(_("Les réferences de la societe"), max_length=100, blank=True, null=True)
    telephone = models.CharField(_("Téléphone"), max_length=50, blank=True, null=True)
    recommande_par = models.CharField(max_length=100, blank=True, null=True)
    visite = models.BooleanField(_("Visite effectuée"), default=False)
    offre_recu = models.BooleanField(_("Candidat a fait une offre"), default=False)

    reponse_questionnaire = models.BooleanField(_("reponse au questionnaire "), default=False)
    proposition_transition = models.BooleanField(_("proposition transition"), default=False)
    propostion_recouverement = models.BooleanField(_("Proposition de recouverement "), default=False)
    contrat_engagement = models.BooleanField(_("contrat engagement "), default=False)
    agence_locale = models.BooleanField(_("Agence locale"), default=False)

    remuneration = models.PositiveIntegerField(blank=True, null=True)
    budget_global = models.PositiveIntegerField(blank=True, null=True)
    budget_securite = models.PositiveIntegerField(blank=True, null=True)
    budget_jardinage = models.PositiveIntegerField(blank=True, null=True)
    budget_picine = models.PositiveIntegerField(blank=True, null=True)
    budget_menage = models.PositiveIntegerField(blank=True, null=True)
    budget_maintenance = models.PositiveIntegerField(blank=True, null=True)
    budget_agent_suivi = models.PositiveIntegerField(blank=True, null=True)
    budget_maitre_nageur = models.PositiveIntegerField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    description = MarkdownxField( blank=True, null=True)    
    comments = GenericRelation(Comment)
    
    @property 
    def total_budget(self) : 
        total = self.budget_agent_suivi + self.budget_jardinage \
                + self.budget_maintenance + self.budget_maitre_nageur \
                + self.budget_menage + self.budget_securite + self.budget_agent_suivi
        return total

    def candidat_comments(self) : 
        return  self.comments.all()

    
    def __str__(self):
        return "%s" % (self.societe)
      
      
class Contacte(models.Model):
    name = models.CharField(max_length=100)
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return "%s" % (self.name)
    
    
class PJEvent(AbstractPieceJointe):
    event = models.ForeignKey('Evenement', on_delete=models.CASCADE)
  

class Evenement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    start       = models.DateTimeField(null=True, blank=True, verbose_name=_('date debut'))
    end         = models.DateTimeField(null=True, blank=True, verbose_name=_('date fin'), default=timezone.now)
    created     = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name=_('created on'))
    closed      = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories  = models.ForeignKey('Category', null=True, blank=True, verbose_name=_('categories'), on_delete=models.SET_NULL)
    comments = GenericRelation(Comment)
    
    def event_comments(self):
        return  self.comments.all()

    class Meta:
        ordering = ('-start',)
        get_latest_by = '-start'
        verbose_name = _('Evenement')
        verbose_name_plural = _('Evenements')

    def __unicode__(self):
        return u'%s' % self.title
    def __str__(self):
        return u'%s' % self.title
    

class Ticket(models.Model):
    """
    Ticket model. Incident
    """
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',  on_delete=models.SET_NULL)
    residence = models.ForeignKey(Residence, related_name='tickets', verbose_name=_('project'), on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField(verbose_name=_('sequence'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(help_text=_("Description"), verbose_name=_('description'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    urgency = models.CharField(max_length=20, choices=TICKET_URGENCY_CHOICES, default=TICKET_DEFAULT_URGENCY, verbose_name=_('urgency'))
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default=TICKET_DEFAULT_STATUS, verbose_name=_('status'))
    created = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name=_('created on'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    due_date        = models.DateTimeField(null=True, blank=True)   # date d'echeance - deadline
    start_date      = models.DateTimeField(null=True, blank=True) # date debut de realisation
    end_date        = models.DateTimeField(null=True, blank=True) # date de fin de realisation
    schedule_date   = models.DateTimeField(null=True, blank=True) # date planifiee

    def __str__(self):
        return self.title

