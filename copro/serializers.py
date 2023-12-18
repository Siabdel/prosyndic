

from rest_framework import serializers
from copro import models as pro_models
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'
# Document
class DocumentApiSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(many=False, read_only=True)
    # author = UserSerializer()

    
    class Meta :
        model = pro_models.PJEtude
        #fields = '__all__'
        fields = ('name', 'piece_name', 'piece_path',
                  'modified', 'created', 'created_by',
                  'init_date_created')
class IncidentApiSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(many=False, read_only=True)
    # author = serializers.SerializerMethodField()
    # author = UserSerializer()

    #documents = DocumentApiSerializer()
    # documents = serializers.StringRelatedField(many=True, read_only=True)
    
    def get_author(self, obj):
        return obj.author.username
    

    class Meta :
        model = pro_models.Ticket
        #fields = '__all__'
        fields  = ('id', 'title', 'comment',  'created_at', 'author', )
   

class ResidenceApiSerializer(serializers.ModelSerializer):
    class Meta :
        model = pro_models.Residence
        fields = '__all__'

## Api Syndic Candidat 
class CandidatApiSerializer(serializers.ModelSerializer):
    class Meta :
        model = pro_models.LigneDeCandidature
        fields = '__all__'