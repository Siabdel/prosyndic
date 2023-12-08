from typing import Any
import datetime
from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView, TemplateView
# local 
from accounts import models as acc_models
from itertools import chain
from rest_framework import generics, permissions
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from cartcom import models as cart_models
from cartcom import serializers as cart_serializ

    
# Document
class ProduitApiList(generics.ListCreateAPIView):
    serializer_class = cart_serializ.ProduitApiSerializer 
    queryset = cart_models.Product.objects.all().order_by('-id')