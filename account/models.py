from django.contrib.auth.models import AbstractUser
from django.db import models

class Organisation(models.Model):
    organisation_code = models.CharField(max_length=50, unique=True)
    organisation_name = models.CharField(max_length=50, unique=True)
    organisation_description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self):
        return f"{self.organisation_name}"

class Job(models.Model):
    job_code = models.CharField(max_length=30, unique=True)
    job_title = models.CharField(max_length=30)
    job_description = models.TextField(blank=True, null=True)
    job_salary = models.FloatField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='jobs', blank=True, null=True)

    def __str__(self):
        return f"{self.job_code} {self.job_title}"


class Person(models.Model):
    cni_number = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    sexe = models.CharField(max_length=30)
    birthday = models.DateField()
    birthplace = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=False)
    matricule = models.CharField(max_length=30, blank=True, null=False)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, related_name='persons', blank=True, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Discipline(models.Model):
    discipline_code = models.CharField(unique=True, max_length=30, blank=True, null=True)
    discipline_date = models.DateField(blank=False, null=False)
    discipline_heure = models.TimeField()
    discipline_motif = models.TextField(blank=True, null=True)
    discipline_date_demande = models.DateTimeField(blank=True, null=True)
    discipline_date_retour = models.DateTimeField(blank=True, null=True)
    discipline_type = models.CharField(blank=False, null=False, max_length=30)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='disciplines', blank=True, null=True)

    def __str__(self):
        return f"{self.discipline_date} : {self.discipline_heure}"

class Localisation(models.Model):
    localisation_code = models.CharField(unique=True, max_length=30, blank=True, null=True)
    localisation_lat = models.FloatField(blank=True, null=True, default=0.0)
    localisation_long = models.FloatField(blank=True, null=True, default=0.0)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='localisations', blank=True, null=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='localisations', blank=True, null=True)

    def __str__(self):
        return f"{self.localisation_lat} : {self.localisation_long}"

class Account(models.Model):
    account_name = models.CharField(max_length=100)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='accounts', blank=True, null=True)

    def __str__(self):
        return self.account_name

class Fonds(models.Model):
    fond_code = models.CharField(max_length=30, unique=True)
    fond_name = models.CharField(max_length=30)
    fond_description = models.CharField(max_length=30)
    started_at = models.DateTimeField(max_length=15, blank=True, null=False)
    ended_at = models.DateTimeField(max_length=30, blank=True, null=False)
    autor = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='author', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self):
        return f"{self.font_name} - {self.parent.font_name}"

class Series(models.Model):
    serie_code = models.CharField(max_length=30, unique=True)
    serie_name = models.CharField(max_length=30)
    serie_description = models.CharField(max_length=30)
    started_at = models.DateTimeField(max_length=15, blank=True, null=False)
    ended_at = models.DateTimeField(max_length=30, blank=True, null=False)
    fond = models.ForeignKey(Fonds, on_delete=models.CASCADE, related_name='series', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self):
        return f"{self.serie_name} - {self.fond.fond_name}"

class Dossiers(models.Model):
    dossier_code = models.CharField(max_length=30, unique=True)
    dossier_label = models.CharField(max_length=30)
    dossier_description = models.CharField(max_length=30, blank=True, null=True)
    started_at = models.DateTimeField(max_length=15, blank=False, null=False)
    ended_at = models.DateTimeField(max_length=30, blank=True, null=True)
    serie = models.ForeignKey(Series, on_delete=models.SET_NULL, related_name='personnes', blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='personnes', blank=True, null=True)

    def __str__(self):
        return f"{self.dossier_code} - {self.dossier_label}"

class Pieces(models.Model):
    piece_code = models.CharField(max_length=30, unique=True)
    piece_title = models.CharField(max_length=30)
    piece_decription = models.CharField(max_length=30)
    file = models.FileField(upload_to='pieces')
    started_at = models.DateTimeField(max_length=15, blank=True, null=False)
    ended_at = models.DateTimeField(max_length=30, blank=True, null=False)
    dossier = models.ForeignKey(Dossiers, on_delete=models.CASCADE, related_name='pieces', blank=True, null=True)

    def __str__(self):
        return f"{self.piece_title}"
