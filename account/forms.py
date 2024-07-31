from django import forms
from .models import Person, Account, Discipline, Localisation

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_name', 'person']
        widgets = {
            'person': forms.Select()  # Pour afficher une liste déroulante des personnes
        }

class PersonForm(forms.ModelForm):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    sexe = forms.ChoiceField(choices=SEXE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Person
        fields = ['cni_number','first_name', 'last_name','sexe','birthday','birthplace', 'email','phone_number','matricule', 'job']
        widgets = {
            'job': forms.Select()
        }

class DisciplineForm(forms.ModelForm):
    type_discipline = [
        ('ABSENCE', 'ABSENCE'),
        ('PERMISSION', 'PERMISSION'),
        ('RETARD', 'RETARD'),
    ]

    discipline_type = forms.ChoiceField(choices=type_discipline, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Discipline
        fields = ['discipline_code','discipline_date', 'discipline_heure','discipline_motif','discipline_date_demande','discipline_date_retour', 'discipline_type', 'person']
        widgets = {
            'person': forms.Select()
        }
class LocalisationForm(forms.ModelForm):
    class Meta:
        model = Localisation
        fields = ['localisation_code','localisation_lat', 'localisation_long', 'discipline', 'person']
        widgets = {
            'person': forms.Select()
        }
