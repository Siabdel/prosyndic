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

now = django.utils.timezone.now()

# Documents pieces jointes
class Document(models.Model):
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
   

class AbstractEnteteDoc(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    documents  = GenericRelation(Document)

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
    created_at = models.DateTimeField(auto_now_add=True)
    # Piece jointe
    documents  = GenericRelation('Document')

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
    
class Piece(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    residence = models.ForeignKey('Residence', on_delete=models.CASCADE)
    piece = models.FileField(upload_to="upload/")
    
class Residence(models.Model):
    name = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(null=True)
    color_code = models.CharField(max_length=6, default="010101")

    class Meta:
        verbose_name = _('Residence')
        verbose_name_plural = _('Residences')
        ordering = ('name',)
    
    def get_pieces_jointe():
        pass
    
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
   
#  Projet 
class Etude(AbstractEnteteDoc):
    title = models.CharField(max_length=200)
    description = models.TextField()
    documents  = GenericRelation(Document)


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
    adresse = models.CharField(max_length=100, blank=True, null=True)
    contacte = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    reference = models.CharField(_("Les réferences de la societe"), max_length=100, blank=True, null=True)
    telephone = models.CharField(_("Téléphone"), max_length=50, blank=True, null=True)
    recommande_par = models.CharField(max_length=100, blank=True, null=True)
    visite = models.BooleanField(_("Visite effectuée"), default='')
    candidat = models.BooleanField(_("Ajouter a la liste des Candidats"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField( blank=True, null=True)    