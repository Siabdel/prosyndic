from django.contrib import admin
from .models import Fournisseur, Document

# Enregistrez le modèle Fournisseur dans l'interface d'administration
admin.site.register(Fournisseur)

# Enregistrez le modèle Document dans l'interface d'administration
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'fournisseur', 'uploaded_at')
    search_fields = ('title', 'fournisseur__nom')  # Recherche par nom de fournisseur
    list_filter = ('fournisseur',)

