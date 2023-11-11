from django.contrib import admin
from accounts import models as acc_models
from django.contrib.auth.admin import UserAdmin

# admin.site.register(User, UserAdmin)

# Register your models here.


@admin.register(acc_models.CustomUser)
class AccountsAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in acc_models.CustomUser._meta.get_fields()]
    list_display = ["username", "first_name", "last_name", "email", "is_staff", "is_superuser",  ]