from django.urls import path
from .views import FormulairePageView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', FormulairePageView.as_view(), name='form')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)