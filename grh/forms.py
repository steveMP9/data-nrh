from django import forms
from account.models import Organisation, Job, Fonds, Series, Dossiers, Pieces

class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ['organisation_code', 'organisation_name', 'organisation_description', 'parent']
        widgets = {
            'parent': forms.Select()
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_code', 'job_title', 'job_description','job_salary','organisation']
        widgets = {
            'organisation': forms.Select()
        }


class FondsForm(forms.ModelForm):
    class Meta:
        model = Fonds
        fields = ['fond_code', 'fond_name', 'fond_description','started_at','ended_at', 'autor','parent']
        widgets = {
            'author': forms.Select(),
            'parent': forms.Select()
        }

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['serie_code', 'serie_name', 'serie_description','started_at','ended_at','fond', 'parent']
        widgets = {
            'fond': forms.Select(),
            'parent': forms.Select()
        }


class DossiersForm(forms.ModelForm):
    class Meta:
        model = Dossiers
        fields = ['dossier_code', 'dossier_label', 'dossier_description','started_at','ended_at', 'serie','person']
        widgets = {
            'serie': forms.Select(),
            'parent': forms.Select()
        }


class PiecesForm(forms.ModelForm):
    class Meta:
        model = Pieces
        fields = ['piece_code', 'piece_title', 'piece_decription','file','started_at','ended_at', 'dossier']
        widgets = {
            'dossier': forms.Select()
        }