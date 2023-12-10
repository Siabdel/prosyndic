

from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from cartcom import models as cart_models

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'

# Document
class ItemArticleSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(many=False, read_only=True)
    # author = UserSerializer()

    
    class Meta :
        model = cart_models.ItemArticle
        #fields = '__all__'
        fields = ('name', 'piece_name', 'piece_path',
                  'modified', 'created', 'created_by',
                  'init_date_created')
        

class ProductApiSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField()
    # author = UserSerializer()
    # documents = serializers.StringRelatedField(many=True, read_only=True)
    
    def get_author(self, obj):
        return obj.author.username
    
    class Meta :
        model = cart_models.Product
        fields = '__all__'
   
class CartOftApiSerializer(serializers.ModelSerializer):
    class Meta :
        model = cart_models.CartOf
        fields = '__all__'