import os
from django.shortcuts import render
from drivedoc import  serializers as  drive_serialize
from drivedoc import  models as drive_models
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from django.http import HttpResponse
from django.conf import settings

# Create your views here.

def render_pdf(request, document_id):
    document = get_object_or_404(drive_models.Document, id=document_id)
    document_path = os.path.join(settings.MEDIA_ROOT, str(document.file))
    with open(document_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')

    # Définir l'en-tête Content-Disposition
    response['Content-Disposition'] = f'inline; filename="{document.title}"'

    # Autoriser l'intégration dans tous les cadres
    response['X-Frame-Options'] =  'ALLOWALL' 

    return response
##
## API 

class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = drive_models.Document.objects.all()
    serializer_class =  drive_serialize.DocumentSerializer


class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = drive_models.Document.objects.all()
    serializer_class = drive_serialize.DocumentSerializer

    def perform_create(self, serializer):
        # Récupérer le fournisseur actuel (vous devez implémenter cette logique selon vos besoins)
        fournisseur_actuel = drive_serialize.Fournisseur.objects.get(nom='NomFournisseur')  # Remplacez 'NomFournisseur' par votre logique

        serializer.save(fournisseur=fournisseur_actuel)


def read_document(request, document_id):
    document = get_object_or_404(drive_models.Document, id=document_id)

    # Construire le chemin absolu du document
    document_path = os.path.join(settings.MEDIA_ROOT, str(document.file))

    # Lire le contenu du document
    with open(document_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')  # Modifier le type de contenu selon le type de fichier

    # Définir les en-têtes pour le téléchargement ou l'affichage
    response['Content-Disposition'] = f'inline; filename="{document.title}"'

    return response

