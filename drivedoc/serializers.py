from rest_framework import serializers
from copro import models as pro_models
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from .models import Document, Fournisseur

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'
# Document
class DocumentApiSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(many=False, read_only=True)
    # author = UserSerializer()

class DocumentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Document
        fields = '__all__'
