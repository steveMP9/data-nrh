from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import OrganisationForm, JobForm, FondsForm, SeriesForm, DossiersForm, PiecesForm
from account.forms import PersonForm, DisciplineForm, LocalisationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from account.models import Organisation, Job, Fonds, Series, Pieces, Person, Dossiers, Discipline, Localisation
from django.views.generic.edit import CreateView
import datetime
import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class GrhPageView(LoginRequiredMixin, TemplateView):
    template_name = 'grh/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grh"] = "active"
        return context

class OrganisationPageView(LoginRequiredMixin, TemplateView):
    template_name_list = 'grh/organisations/organisation_liste.html'
    template_name_form = 'grh/organisations/organisation_form.html'
    template_name_detail = 'grh/organisations/organisation_detail.html'

    def get(self, request, *args, **kwargs):
        if 'create' in request.path:
            form = OrganisationForm()
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Create'
            })
        elif 'update' in request.path:
            organisation_id = kwargs.get('pk')
            organisation = get_object_or_404(Organisation, pk=organisation_id)
            form = OrganisationForm(instance=organisation)
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Update',
                'organisation_id': organisation_id
            })
        elif 'detail' in request.path:
            organisation_id = kwargs.get('pk')
            organisation = get_object_or_404(Organisation, pk=organisation_id)
            return render(request, self.template_name_detail, {
                'organisation': organisation,
                'action': 'Detail',
            })
        else:
            organisations = Organisation.objects.all()
            return render(request, self.template_name_list, {
                'organisations': organisations,
                'action': 'List'
            })



    def post(self, request, *args, **kwargs):
        form = None
        organisation_id = kwargs.get('pk')

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            return self.delete(request, *args, **kwargs)

        if 'create' in request.path:
            form = OrganisationForm(request.POST)

        elif 'update' in request.path:
            organisation = get_object_or_404(Organisation, pk=organisation_id)
            form = OrganisationForm(request.POST, instance=organisation)

        if form.is_valid():
            form.save()
            return redirect('organisation_list')  # Redirige vers la liste après la soumission

        action = 'Update' if 'update' in request.path else 'Create'
        return render(request, self.template_name_form, {
            'form': form,
            'action': action,
            'organisation_id': organisation_id if 'update' in request.path else None
        })


    def delete(self, request, *args, **kwargs):
        organisation_id = kwargs.get('pk')
        organisation = get_object_or_404(Organisation, pk=organisation_id)
        organisation.delete()
        return redirect('organisation_list')

class JobPageView(LoginRequiredMixin, TemplateView):
    template_name_list = 'grh/jobs/job_liste.html'
    template_name_form = 'grh/jobs/job_form.html'
    template_name_detail = 'grh/jobs/job_detail.html'

    def get(self, request, *args, **kwargs):
        if 'create' in request.path:
            form = JobForm()
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Create'
            })
        elif 'update' in request.path:
            job_id = kwargs.get('pk')
            job = get_object_or_404(Job, pk=job_id)
            form = JobForm(instance=job)
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Update',
                'job_id': job_id
            })
        elif 'detail' in request.path:
            job_id = kwargs.get('pk')
            job = get_object_or_404(Job, pk=job_id)
            return render(request, self.template_name_detail, {
                'job': job,
                'action': 'Detail',
            })
        else:
            jobs = Job.objects.all()
            return render(request, self.template_name_list, {
                'jobs': jobs,
                'action': 'List'
            })



    def post(self, request, *args, **kwargs):
        form = None
        job_id = kwargs.get('pk')

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            return self.delete(request, *args, **kwargs)

        if 'create' in request.path:
            form = JobForm(request.POST)

        elif 'update' in request.path:
            job = get_object_or_404(Job, pk=job_id)
            form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirige vers la liste après la soumission

        action = 'Update' if 'update' in request.path else 'Create'
        return render(request, self.template_name_form, {
            'form': form,
            'action': action,
            'job_id': job_id if 'update' in request.path else None
        })


    def delete(self, request, *args, **kwargs):
        job_id = kwargs.get('pk')
        job = get_object_or_404(Organisation, pk=job_id)
        job.delete()
        return redirect('job_list')

class DossierPageView(LoginRequiredMixin, TemplateView):
    template_name_list = 'grh/planclassement/dossier/dossier_liste.html'
    template_name_form = 'grh/planclassement/dossier/dossier_form.html'
    template_name_detail = 'grh/planclassement/dossier/dossier_detail.html'

    def get(self, request, *args, **kwargs):

        sexe_choice = [
            ('M', 'Masculin'),
            ('F', 'Féminin'),
        ]
        jobs = Job.objects.all()

        if 'create' in request.path:
            code = self.code_dossier()
            numeroDossier = code[0]
            numeroMatricule = code[1]
            initial_data = {'dossier_code': numeroDossier, 'matricule': numeroMatricule}
            form = DossiersForm(initial=initial_data)
            form2 = PersonForm(initial=initial_data)

            return render(request, self.template_name_form, {
                'form': form,
                'form2': form2,
                'jobs': jobs,
                'sexes': sexe_choice,
                'action': 'Create'
            })
        elif 'update' in request.path:
            dossier_id = kwargs.get('pk')
            dossier = get_object_or_404(Dossiers, pk=dossier_id) if dossier_id else None
            form = DossiersForm(instance=dossier)
            person = get_object_or_404(Person, pk=dossier.person_id) if dossier.person_id else None
            form2 = PersonForm(instance=person)
            print(person.job)
            return render(request, self.template_name_form, {
                'form': form,
                'form2': form2,
                'jobs': jobs,
                'sexes': sexe_choice,
                'action': 'Update',
                'dossier_id': dossier_id
            })
        elif 'detail' in request.path:
            dossier_id = kwargs.get('pk')
            dossier = get_object_or_404(Dossiers, pk=dossier_id)
            return render(request, self.template_name_detail, {
                'dossier': dossier,
                'action': 'Detail',
            })
        else:
            dossiers = Dossiers.objects.all()
            return render(request, self.template_name_list, {
                'dossiers': dossiers,
                'action': 'List'
            })


    def post(self, request, *args, **kwargs):
        form = None
        dossier_id = kwargs.get('pk')

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            return self.delete(request, *args, **kwargs)

        if 'create' in request.path:
            person_form = PersonForm(request.POST)
            dossier_form = DossiersForm(request.POST)
            if person_form.is_valid() and dossier_form.is_valid():
                person = person_form.save()
                dossier = dossier_form.save(commit=False)
                dossier.person = person
                dossier.save()

                return redirect('dossier_list')  # Redirige vers la liste après la soumission
            else:
                print(person_form.errors, dossier_form.errors)

        elif 'update' in request.path:
            current_dossier = get_object_or_404(Dossiers, pk=dossier_id)
            person_form = PersonForm(request.POST, instance=current_dossier.person)
            dossier_form = DossiersForm(request.POST, instance=current_dossier)
            if person_form.is_valid() and dossier_form.is_valid():
                person = person_form.save()
                dossier = dossier_form.save(commit=False)
                dossier.person = person
                dossier.save()
                return redirect('dossier_list')  # Redirige vers la liste après la soumission

        sexe_choice = [('M', 'Masculin'),('F', 'Féminin'),]
        jobs = Job.objects.all();
        action = 'Update' if 'update' in request.path else 'Create'
        return render(request, self.template_name_form, {
            'form': dossier_form,
            'form2': person_form,
            'sexes': sexe_choice,
            'jobs': jobs,
            'action': action,
            'dossier_id': dossier_id if 'update' in request.path else None
        })


    def delete(self, request, *args, **kwargs):
        dossier_id = kwargs.get('pk')
        dossier = get_object_or_404(Dossiers, pk=dossier_id)
        dossier.delete()
        return redirect('dossier_list')

    def code_dossier(self):
        current_year = datetime.datetime.now().year
        prefix = f"{current_year}."

        # Récupérer le dernier code pour l'année en cours
        last_dossier = Dossiers.objects.filter(dossier_code__startswith=prefix).order_by('-dossier_code').first()

        if last_dossier:
            last_code = last_dossier.dossier_code
            last_number = int(last_code.split('.')[1])
            new_number = last_number + 1
        else:
            new_number = 1

        # Générer le nouveau code avec 5 chiffres pour la partie code
        new_code = f"{current_year}.{str(new_number).zfill(5)}"
        matricule = f"{str(new_number).zfill(5)}{current_year}"
        return [new_code, matricule]

class DisciplinePageView(LoginRequiredMixin, TemplateView):
    template_name_list = 'grh/discipline/liste.html'
    template_name_form = 'grh/discipline/form.html'
    template_name_detail = 'grh/discipline/dossier_detail.html'

    def get(self, request, *args, **kwargs):

        persons = Person.objects.all()
        type_discipline = [
            ('ABSENCE', 'ABSENCE'),
            ('PERMISSION', 'PERMISSION'),
            ('RETARD', 'RETARD'),
        ]

        if 'create' in request.path:
            form = DisciplineForm()
            return render(request, self.template_name_form, {
                'form': form,
                'types': type_discipline,
                'persons': persons,
                'action': 'Create'
            })
        elif 'update' in request.path:
            discipline_id = kwargs.get('pk')
            discipline = get_object_or_404(Discipline, pk=discipline_id) if discipline_id else None
            form = DisciplineForm(instance=discipline)
            return render(request, self.template_name_form, {
                'form': form,
                'types': type_discipline,
                'persons': persons,
                'action': 'Update',
                'discipline_id': discipline_id
            })
        elif 'detail' in request.path:
            discipline_id = kwargs.get('pk')
            discipline = get_object_or_404(Discipline, pk=discipline_id)
            return render(request, self.template_name_detail, {
                'discipline': discipline,
                'action': 'Detail',
            })
        else:
            discipline = Discipline.objects.all()
            return render(request, self.template_name_list, {
                'disciplines': discipline,
                'action': 'List'
            })


    def post(self, request, *args, **kwargs):
        form = None
        discipline_id = kwargs.get('pk')
        type_discipline = [
            ('ABSENCE', 'ABSENCE'),
            ('PERMISSION', 'PERMISSION'),
            ('RETARD', 'RETARD'),
        ]

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            return self.delete(request, *args, **kwargs)

        if 'create' in request.path:
            form = DisciplineForm(request.POST)
            if form.is_valid():
                discipline = form.save(commit=False)
                discipline.discipline_code = self.generate_code()
                discipline.save()
                return redirect('discipline_list')  # Redirige vers la liste après la soumission
            else:
                print(form.errors)

        elif 'update' in request.path:
            current_discipline = get_object_or_404(Discipline, pk=discipline_id)
            form = DisciplineForm(request.POST, instance=current_discipline)
            if form.is_valid():
                current_discipline = Discipline.objects.filter(pk=discipline_id).order_by('-discipline_code').first()
                discipline = form.save(commit=False)
                discipline.discipline_code = current_discipline.discipline_code
                discipline.save()
                return redirect('discipline_list')  # Redirige vers la liste après la soumission

        action = 'Update' if 'update' in request.path else 'Create'
        return render(request, self.template_name_form, {
            'form': form,
            'types': type_discipline,
            'action': action,
            'dossier_id': discipline_id if 'update' in request.path else None
        })


    def delete(self, request, *args, **kwargs):
        discipline_id = kwargs.get('pk')
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        discipline.delete()
        return redirect('discipline_list')

    def generate_code(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        sec = datetime.datetime.now().second
        mics = datetime.datetime.now().microsecond
        code = f"{mics}{minute}{sec}{month}{day}{hour}{year}"
        return code

class PresencePageView(LoginRequiredMixin, TemplateView):
    template_name_form = 'grh/discipline/form.html'

    def get(self, request, *args, **kwargs):
        form = LocalisationForm()
        return render(request, self.template_name_form, {
            'form': form,
            'action': 'Create'
        })


    def post(self, request, *args, **kwargs):
        form = LocalisationForm(request.POST)
        if form.is_valid():
            discipline_form = DisciplineForm()
            discipline = discipline_form.save(commit=False)
            discipline.discipline_code = self.generate_code()
            discipline.discipline_type = "PRENSENCE"
            discipline.discipline_date = datetime.datetime.now()
            discipline.discipline_heure = datetime.datetime.now().time()
            discipline.discipline_motif = "RAS"
            discipline.save()

            localisation = form.save(commit=False)
            localisation.localisation_code = self.generate_code()
            localisation.localisation_lat = 0.0
            localisation.localisation_long = 0.0
            localisation.discipline = discipline
            localisation.save()

            return redirect('localisation_presence')  # Redirige vers la liste après la soumission

        action = 'Create'
        return render(request, self.template_name_form, {
            'form': form,
            'action': action,
        })

    def generate_code(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        sec = datetime.datetime.now().second
        mics = datetime.datetime.now().microsecond
        code = f"{mics}{minute}{sec}{month}{day}{hour}{year}"
        return code

class SeriePageView(LoginRequiredMixin, TemplateView):
    template_name_list = 'grh/planclassement/serie/serie_liste.html'
    template_name_form = 'grh/planclassement/serie/serie_form.html'
    template_name_detail = 'grh/planclassement/serie/serie_detail.html'

    def get(self, request, *args, **kwargs):
        if 'create' in request.path:
            form = SeriesForm()
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Create'
            })
        elif 'update' in request.path:
            serie_id = kwargs.get('pk')
            serie = get_object_or_404(Organisation, pk=serie_id)
            form = SeriesForm(instance=serie)
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Update',
                'serie_id': serie_id
            })
        elif 'detail' in request.path:
            serie_id = kwargs.get('pk')
            serie = get_object_or_404(Organisation, pk=serie_id)
            return render(request, self.template_name_detail, {
                'serie': serie,
                'action': 'Detail',
            })
        else:
            series = Series.objects.all()
            return render(request, self.template_name_list, {
                'series': series,
                'action': 'List'
            })



    def post(self, request, *args, **kwargs):
        form = None
        serie_id = kwargs.get('pk')

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            return self.delete(request, *args, **kwargs)

        if 'create' in request.path:
            form = SeriesForm(request.POST)

        elif 'update' in request.path:
            serie = get_object_or_404(Organisation, pk=serie_id)
            form = SeriesForm(request.POST, instance=serie)

        if form.is_valid():
            form.save()
            return redirect('serie_list')  # Redirige vers la liste après la soumission

        action = 'Update' if 'update' in request.path else 'Create'
        return render(request, self.template_name_form, {
            'form': form,
            'action': action,
            'serie_id': serie_id if 'update' in request.path else None
        })


    def delete(self, request, *args, **kwargs):
        serie_id = kwargs.get('pk')
        serie = get_object_or_404(Organisation, pk=serie_id)
        serie.delete()
        return redirect('serie_list')

class FondPageView(LoginRequiredMixin, TemplateView):
    template_name_list = 'grh/planclassement/fond/fond_liste.html'
    template_name_form = 'grh/planclassement/fond/fond_form.html'
    template_name_detail = 'grh/planclassement/fond/fond_detail.html'

    def get(self, request, *args, **kwargs):
        if 'create' in request.path:
            form = FondsForm()
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Create'
            })
        elif 'update' in request.path:
            fond_id = kwargs.get('pk')
            fond = get_object_or_404(Organisation, pk=fond_id)
            form = FondsForm(instance=fond)
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Update',
                'fond_id': fond_id
            })
        elif 'detail' in request.path:
            fond_id = kwargs.get('pk')
            fond = get_object_or_404(Organisation, pk=fond_id)
            return render(request, self.template_name_detail, {
                'fond': fond,
                'action': 'Detail',
            })
        else:
            fonds = Fonds.objects.all()
            return render(request, self.template_name_list, {
                'fonds': fonds,
                'action': 'List'
            })



    def post(self, request, *args, **kwargs):
        form = None
        fond_id = kwargs.get('pk')

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            return self.delete(request, *args, **kwargs)

        if 'create' in request.path:
            form = FondsForm(request.POST)

        elif 'update' in request.path:
            fond = get_object_or_404(Organisation, pk=fond_id)
            form = FondsForm(request.POST, instance=fond)

        if form.is_valid():
            form.save()
            return redirect('fond_list')  # Redirige vers la liste après la soumission

        action = 'Update' if 'update' in request.path else 'Create'
        return render(request, self.template_name_form, {
            'form': form,
            'action': action,
            'fond_id': fond_id if 'update' in request.path else None
        })


    def delete(self, request, *args, **kwargs):
        fond_id = kwargs.get('pk')
        fond = get_object_or_404(Organisation, pk=fond_id)
        fond.delete()
        return redirect('fond_list')

class PiecePageView(LoginRequiredMixin, TemplateView):
    template_name_list = 'grh/planclassement/piece/piece_liste.html'
    template_name_form = 'grh/planclassement/piece/piece_form.html'
    template_name_detail = 'grh/planclassement/piece/piece_detail.html'

    def get(self, request, *args, **kwargs):
        if 'create' in request.path:
            form = PiecesForm()
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Create'
            })
        elif 'update' in request.path:
            piece_id = kwargs.get('pk')
            piece = get_object_or_404(Organisation, pk=piece_id)
            form = PiecesForm(instance=piece)
            return render(request, self.template_name_form, {
                'form': form,
                'action': 'Update',
                'piece_id': piece_id
            })
        elif 'detail' in request.path:
            piece_id = kwargs.get('pk')
            piece = get_object_or_404(Organisation, pk=piece_id)
            return render(request, self.template_name_detail, {
                'piece': piece,
                'action': 'Detail',
            })
        else:
            pieces = Organisation.objects.all()
            return render(request, self.template_name_list, {
                'pieces': pieces,
                'action': 'List'
            })



    def post(self, request, *args, **kwargs):
        form = None
        piece_id = kwargs.get('pk')

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            return self.delete(request, *args, **kwargs)

        if 'create' in request.path:
            form = PiecesForm(request.POST)

        elif 'update' in request.path:
            piece = get_object_or_404(Organisation, pk=piece_id)
            form = PiecesForm(request.POST, instance=piece)

        if form.is_valid():
            form.save()
            return redirect('piece_list')  # Redirige vers la liste après la soumission

        action = 'Update' if 'update' in request.path else 'Create'
        return render(request, self.template_name_form, {
            'form': form,
            'action': action,
            'piece_id': piece_id if 'update' in request.path else None
        })


    def delete(self, request, *args, **kwargs):
        piece_id = kwargs.get('pk')
        piece = get_object_or_404(Organisation, pk=piece_id)
        piece.delete()
        return redirect('piece_list')