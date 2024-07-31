from django.urls import path
from .views import GrhPageView, OrganisationPageView, JobPageView, FondPageView, SeriePageView, DossierPageView, PiecePageView, DisciplinePageView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', GrhPageView.as_view(), name='grh'),
    path('organisation/', OrganisationPageView.as_view(), name='organisation_list'),  # Liste des organisation
    path('organisation/detail/<int:pk>/', OrganisationPageView.as_view(), name='organisation_detail'),  # Détails d'une organisation
    path('organisation/create/', OrganisationPageView.as_view(), name='create_organisation'),  # Créer une organisation
    path('organisation/update/<int:pk>/', OrganisationPageView.as_view(), name='update_organisation'),  # Modifier une organisation
    path('organisation/delete/<int:pk>/', OrganisationPageView.as_view(), name='delete_organisation'),  # Supprimer une organisation

    path('job/', JobPageView.as_view(), name='job_list'),  # Liste des job
    path('job/detail/<int:pk>/', JobPageView.as_view(), name='job_detail'),  # Détails d'un job
    path('job/create/', JobPageView.as_view(), name='create_job'),  # Créer un job
    path('job/update/<int:pk>/', JobPageView.as_view(), name='update_job'),  # Modifier un job
    path('job/delete/<int:pk>/', JobPageView.as_view(), name='delete_job'),  # Supprimer un job

    path('fond/', FondPageView.as_view(), name='fond_list'),  # Liste des fond
    path('fond/detail/<int:pk>/', FondPageView.as_view(), name='fond_detail'),  # Détails d'un fond
    path('fond/create/', FondPageView.as_view(), name='create_fond'),  # Créer un fond
    path('fond/update/<int:pk>/', FondPageView.as_view(), name='update_fond'),  # Modifier un fond
    path('fond/delete/<int:pk>/', FondPageView.as_view(), name='delete_fond'),  # Supprimer un fond

    path('serie/', SeriePageView.as_view(), name='serie_list'),  # Liste des serie
    path('serie/detail/<int:pk>/', SeriePageView.as_view(), name='serie_detail'),  # Détails d'une serie
    path('serie/create/', SeriePageView.as_view(), name='create_serie'),  # Créer une serie
    path('serie/update/<int:pk>/', SeriePageView.as_view(), name='update_serie'),  # Modifier une serie
    path('serie/delete/<int:pk>/', SeriePageView.as_view(), name='delete_serie'),  # Supprimer une serie

    path('dossier/', DossierPageView.as_view(), name='dossier_list'),  # Liste des dossier
    path('dossier/detail/<int:pk>/', DossierPageView.as_view(), name='dossier_detail'),  # Détails d'un dossier
    path('dossier/create/', DossierPageView.as_view(), name='create_dossier'),  # Créer un dossier
    path('dossier/update/<int:pk>/', DossierPageView.as_view(), name='update_dossier'),  # Modifier un dossier
    path('dossier/delete/<int:pk>/', DossierPageView.as_view(), name='delete_dossier'),  # Supprimer un dossier

    path('piece/', PiecePageView.as_view(), name='piece_list'),  # Liste des piece
    path('piece/detail/<int:pk>/', PiecePageView.as_view(), name='piece_detail'),  # Détails d'une piece
    path('piece/create/', PiecePageView.as_view(), name='create_piece'),  # Créer une piece
    path('piece/update/<int:pk>/', PiecePageView.as_view(), name='update_piece'),  # Modifier une piece
    path('piece/delete/<int:pk>/', PiecePageView.as_view(), name='delete_piece'),  # Supprimer une piece

    path('discipline/', DisciplinePageView.as_view(), name='discipline_list'),  # Liste des piece
    path('discipline/detail/<int:pk>/', DisciplinePageView.as_view(), name='discipline_detail'),  # Détails d'une piece
    path('discipline/create/', DisciplinePageView.as_view(), name='create_discipline'),  # Créer une piece
    path('discipline/update/<int:pk>/', DisciplinePageView.as_view(), name='update_discipline'),  # Modifier une piece
    path('discipline/delete/<int:pk>/', DisciplinePageView.as_view(), name='delete_discipline'),  # Supprimer une piece

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)