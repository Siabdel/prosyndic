from django.db import models
import os, json
import datetime
import time
import django
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from markdownx.models import MarkdownxField
from django.utils import timezone
from django.core import serializers


class Fournisseur(models.Model):
    nom = models.CharField(max_length=255)
    # Ajoutez d'autres champs spécifiques au fournisseur selon vos besoins

    def __str__(self):
        return self.nom


class Document(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)  # Utilisez le modèle Fournisseur

    def __str__(self):
        return self.title
