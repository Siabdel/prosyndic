
from rest_framework import serializers
from .models import Rubrique, SousRubrique, ChargesFonctionnement

class RubriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubrique
        fields = '__all__'

class SousRubriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousRubrique
        fields = '__all__'

class ChargesFonctionnementSerializer(serializers.ModelSerializer):
    sous_rubrique = SousRubriqueSerializer()

    class Meta:
        model = ChargesFonctionnement
        fields = '__all__'
