# -*- coding:UTF-8 -*-
import re
import datetime
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList, ValidationError, ErrorDict
# translate
from django.utils.translation import gettext as _
from django.forms.models import inlineformset_factory
from cartcom import models as cart_models

DURATION_WIDGET_OPTIONS = {
    'format': 'hh:ii',
    'minuteStep': 15,
}
#--------------------------
w_titre = forms.TextInput(attrs={'size': 100, 'class': 'form-control'})
w_slug = forms.TextInput(attrs={'size': 50,  'class': 'form-control'})
text_widget = forms.TextInput(attrs={'size': 40, 'class': 'form-control'})
contenu_widget = forms.Textarea(
    attrs={'cols': 80, 'rows': 12, 'class': 'form-control'})
w_radio_select = forms.RadioSelect(attrs={'class': 'radio'})


semaine_aujourdhui = datetime.datetime.isocalendar(datetime.datetime.now())[1]
SEMAINES_CHOICE = [(sem, sem) for sem in range(semaine_aujourdhui, 53, 1)]
# -- formulaire de recherche Medecin
query_machines = cart_models.ItemArticle.objects.all()
JOURS_SEMAINE = [(1, 'lundi'), (2, 'mardi', ), (3, 'mercredi'),
                 (4, 'jeudi'),  (5, 'vendredi'), (7, 'samedi')]


#---------------------------------
# validation de champ telephone
#---------------------------------
def format_validator(value):
    if not re.match("([a-z]+[ ]*[,][ ]*)+([a-z]+[ ]*)$", value):
        raise ValidationError(u'mauvais format saisie !!')

def format_validator_semaine(value):
    if not re.match("([\d]{2})$", value):
        raise ValidationError(u'mauvais samine saisie !!')



# contruction list
queryset = cart_models.ItemArticle.objects.none(),
query_machine = cart_models.ItemArticle.objects.all()

class SearchMachineForm(forms.Form):
    # cle_recherche = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size':30}))
    choices=JOURS_SEMAINE
    ###

   

# ------------------------------------
# -- formulaire de recherche Medecin
# ------------------------------------


class SearchDacForm(forms.Form):

    cle_recherche = forms.CharField(max_length=50,
                widget=forms.TextInput(attrs={'size': 60}))

    semaines = forms.CharField(widget=forms.Select(
        choices=SEMAINES_CHOICE), initial='16')

    def __init__(self, *args, **kwargs):
        # appel a la class mère
        super(SearchDacForm, self).__init__(*args, **kwargs)
        # charger les parametre semaine et annee
        # set the user_id as an attribute of the form

        # charger la class bootstrap
        for key, field in self.fields.items():
            if field:
                field.widget.attrs['class'] = 'form-control'
                if field.label:
                    field.label = ugettext(field.label)  # traduire le label
                # les input

                if type(field.widget) in (forms.Select, forms.TextInput,
                                          forms.SelectMultiple,
                                          forms.DateInput):
                    field.widget.attrs['class'] = 'input-lg'
                    # charger place holder
                    field.widget.attrs['placeholder'] = field.label

    class Meta:
        ordering = ('-created',)


class CommentDaForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':80}), label='Commentaire' )

    def __init__(self,  *args, **kwargs):
        # appel a la class mère
        super(CommentDaForm, self).__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
            # We have initial arguments, fetch 'user' placeholder variable if any
            user = initial_arguments.get('user',None)
            # Now update the form's initial values if user  getattr(user, 'email', None)
            updated_initial['comment'] = "toto  ...."

        # set the cac_id as an attribute of the form
        # You can also initialize form fields with hardcoded values
        # or perform complex DB logic here to then perform initialization
        updated_initial['comment'] = 'Please provide a comment'
        # Finally update the kwargs initial reference
        kwargs.update(initial=updated_initial)
        # self.fields['cac_id'].initial = 33


    def save_(self, commit=True):
        # code here

        # 1/ sauvergarde commande DA
        enreg =  super(CommentDaForm, self).save(commit)
        enreg.save()

        # 2/ sauvegarder les commentaire dans entete approv
        entete_da = models.DjangoEnteteAppro.objects.get(cac_id=enreg.pk)
        entete_da.comment = enreg.comment
        entete_da.save()
