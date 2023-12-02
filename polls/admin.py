from django.contrib import admin
from polls import models as pll_models

class UserVoteInline(admin.TabularInline):
    model = pll_models.UserVote
    extra = 8


@admin.register(pll_models.Campagne)
class CampagneAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['titre']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [UserVoteInline]
    list_display = ('titre', 'pub_date', )
    list_filter = ['pub_date']
    search_fields = ['titre']

@admin.register(pll_models.Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display  = ['question', 'q_type', 'active']


@admin.register(pll_models.QualifiedChoice)
class QualifiedChoiceAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in pll_models.QualifiedChoice._meta.get_fields()]
    list_display  = ['code', 'name', 'positif', 's_valeur', 'active',  ]

@admin.register(pll_models.UserVote)
class UserVoteAdmin(admin.ModelAdmin):
    list_display  = ['campagne', 'question', 'vote', 'created_by', 'created',   ]
