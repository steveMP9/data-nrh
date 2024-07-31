from django.urls import path
from .views import HomePageView, DataPageView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='dashboad'),
    path('dashboard/donnees', DataPageView.as_view(), name='donnees'),
    path('dashboard/donnees-ajax', DataPageView.as_view(), name='dataList'),
    path('dashboard/uploads', DataPageView.as_view(), name='upload'),
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
