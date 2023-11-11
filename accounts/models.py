from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class CustomUser(AbstractUser):
    pass
    class Meta(AbstractUser.Meta):
         swappable = "AUTH_USER_MODEL"


