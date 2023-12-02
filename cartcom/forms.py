# -*- coding:UTF-8 -*-
import re
import datetime
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms.utils import ErrorList, ValidationError, ErrorDict
from ofschedule import models
# translate
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.models import inlineformset_factory
from approvisionnement import models

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
query_machines = models.DjangoMachine.objects.filter(
    nommach__in=['INCONNU', 'A14'])
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
queryset = models.DjangoMachine.objects.none(),

query_machine = models.DjangoMachine.objects.all().values_list('codemach', 'nommach').distinct()

machines_de_semaine = [(machine_travail_id__codemach, machine_travail_id__nommach)
            for (machine_travail_id__codemach, machine_travail_id__nommach)
            in query_machine.iterator()]

machines_de_semaine = machines_de_semaine + [('', 'None')]

class SearchMachineForm(forms.Form):

    # cle_recherche = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size':30}))

    machines = forms.ChoiceField(label='Machines',choices=machines_de_semaine, required=False)

    # machines_semaine = [ (choice.pk, choice) for choice in models.DjangoMachine.objects.filter(pk__in =
    #semaines = forms.CharField(widget=forms.Select( choices=SEMAINES_CHOICE), required=True)
    semaine = forms.CharField(max_length=2, required=False)
    annee   = forms.CharField(max_length=4, required=False)
    #
    jours_semaine = forms.MultipleChoiceField(required=False,
                                        widget=forms.CheckboxSelectMultiple,
                                        choices=JOURS_SEMAINE)
    #
    jours_semaine.widget.attrs.update({'class': 'input-lg' })

    semaine.widget.attrs.update({'class': 'input-lg', 'size':'2'})
    machines.widget.attrs.update({'class': 'input-lg', 'v-model':'current_machine' })


    def __init__(self,  *args, **kwargs):
        # appel a la class mère
        super(SearchMachineForm, self).__init__(*args, **kwargs)
        # set the user_id as an attribute of the form
        #self.fields['semaine'].initial = 33
        self.fields['machines'].choices= machines_de_semaine
        self.fields['machines'].widget.attrs['v-model'] = 'current_machine'

        # charger la class bootstrap
        for key, field in self.fields.items():
            if field:
                if field.label:
                    field.label = ugettext(field.label)  # traduire le label
                # les input

                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget.attrs['class'] = 'input-lg'
                    # charger place holder
                    field.widget.attrs['placeholder'] = field.label
                elif type(field.widget) in (forms.Select, forms.SelectMultiple ):
                    field.widget.attrs['v-model'] = 'current_machine'
                    field.widget.attrs['class'] = 'input-lg'

    class Meta:
        ordering = ('nommach',)

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
