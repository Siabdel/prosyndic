import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Campagne(models.Model):
    titre = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.titre

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    # was_published_recently.admin_order_field = 'pub_date'
    # was_published_recently.boolean = True
    # was_published_recently.short_description = 'Published recently?'
    
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class QualifiedChoice(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    positif = models.BooleanField(_('qualite positif'))
    s_valeur = models.PositiveIntegerField(_('sa valeur'))
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    class QuestionnaireType(models.TextChoices):
        SATISFACT = 'SAT', _('Questionnaire Satisfaction')
        ELECTORAL = 'ELC', _('Questionnaire Electorale')
        CANDIDAT = 'CAND', _('Questionnaire Candidature')
        
    question = models.CharField(max_length=100)
    q_type = models.CharField(max_length=50, 
                            choices = QuestionnaireType.choices,
                            default=QuestionnaireType.CANDIDAT)
    
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    
    
class UserVote(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    question = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    vote = models.ForeignKey(QualifiedChoice, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta :
        unique_together = ('campagne', 'created_by', 'question', 'vote', )

    def __str__(self):
        return "{} - {}".format(self.question, self.vote)

    def get_absolute_url(self):
        return reverse("polls:detail", kwargs={"pk": self.pk})
