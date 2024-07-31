import os
import json
import io, base64, urllib
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split,KFold, LeaveOneOut, ShuffleSplit, StratifiedKFold, StratifiedShuffleSplit
import sklearn
from sklearn.metrics import classification_report ,precision_score, recall_score, roc_auc_score,confusion_matrix ,accuracy_score
from sklearn.linear_model import LogisticRegression
import warnings
from django.views.generic import TemplateView
from .forms import UploadFileForm
import json
from django.contrib.auth.mixins import LoginRequiredMixin

warnings.filterwarnings("ignore")

# Create your views here.
class HomePageView(LoginRequiredMixin, TemplateView):

    template_name = 'datas/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["home"] = "active"
        return context

class DataPageView(LoginRequiredMixin, TemplateView):
    template_name = "datas/datas.html"

    def get_context_data(self, **kwargs):
        dataset = self.loaddata()
        context = super().get_context_data(**kwargs)

        context["datas"] = "active"
        context["data_table"] = dataset.to_dict(orient='records')
        context["datahead"] = dataset.columns.tolist()
        context["form"] = UploadFileForm()
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            dataset_imported = self.loaddata()
            dataset_imported.columns = [col.replace('.', '_') for col in dataset_imported.columns]
            dtypes = dataset_imported.dtypes
            columnsTypes = {'Colonnes': dtypes.index.tolist(), 'Types': dtypes.values.astype(str).tolist()}

            return JsonResponse({"columns": dataset_imported.columns.tolist(), "datas": dataset_imported.to_dict(orient="records"), "dataSize": dataset_imported.shape, "columnsTypes": columnsTypes}, safe=False)
        else:
            return self.render_to_response(self.get_context_data())


    def loaddata(self):
        dataset = dict()
        with open(os.path.join(settings.MEDIA_ROOT, 'logs/log.json'), 'r') as fichier:
            logs_json = json.load(fichier)
            context = {}
            for cle in logs_json:
                logs = logs_json[cle]
                print(logs)
            if len(logs_json)>0:
                cle = list(logs_json)[-1]
                logs = logs_json[cle]
                
                if(os.path.join(settings.MEDIA_ROOT, logs[0])):
                    dataset = pd.read_csv(os.path.join(settings.MEDIA_ROOT, "datas\\"+logs[0]), sep=",", encoding='Latin-1')
                    empty_columns = dataset.columns[dataset.isnull().all()]
                    if not empty_columns.empty:
                        df_cleaned = dataset.drop(columns=empty_columns)
                        df_cleaned.fillna("-", inplace=True)
                        return df_cleaned
                    return dataset
        return dataset

    def loadnewdata(self):
        dataset = dict()
        if(os.path.join(settings.MEDIA_ROOT, "newdataset.xlsx")):
            dataset = pd.read_excel(os.path.join(settings.MEDIA_ROOT, "newdataset.xlsx"), index_col=None)
        return dataset

    def loadnewdata_dummy(self):
        dataset = dict()
        if(os.path.join(settings.MEDIA_ROOT, "dummydataset.csv")):
            dataset = pd.read_excel(os.path.join(settings.MEDIA_ROOT, "dummydataset.csv"), index_col=None)
        return dataset

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            self._handle_uploaded_file(request.FILES['file'])
            messages.success(request, 'File uploaded successfully!')
            return redirect("donnees")
        messages.error(request, 'Error uploading file. Please try again.')
        return self.render_to_response(self.get_context_data(form=form, error=True))

    def _handle_uploaded_file(self, f):
        if not os.path.exists(f"{settings.MEDIA_ROOT}/datas"):
            os.makedirs(f"{settings.MEDIA_ROOT}/datas")
        
        original_name, file_extension = os.path.splitext(f.name)
        new_name = f"data_{datetime.now().strftime('%Y%m%d%H%M%S')}{file_extension}"

        with open(os.path.join(settings.MEDIA_ROOT, 'logs/log.json'), 'r') as fichier:
            logs_json = json.load(fichier)
                
        with open(os.path.join(settings.MEDIA_ROOT, 'logs/log.json'), 'w') as fichiers:
            now = datetime.now().strftime("%d%m%Y%H%M%S")
            upload_path = os.path.join(f"{settings.MEDIA_ROOT}/datas", new_name)
                
            logs_json["title"+now] = [new_name]
            json.dump(logs_json, fichiers,indent=4, ensure_ascii=False, sort_keys=False )

            with open(upload_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        
        return {'new_name': new_name, 'file_extension': file_extension}
    
    def apply_filters(self, df, filters):
        # # Appliquer les filtres sur le DataFrame
        # for col, filter_value in filters.items():
        #     if col == 'Âge':
        #         if filter_value == 'Jeune':
        #             df = df[df[col] < 20]
        #         elif filter_value == 'Moyen':
        #             df = df[(df[col] >= 20) & (df[col] <= 25)]
        #         elif filter_value == 'Vieux':
        #             df = df[df[col] > 25]
        #     # Ajoutez d'autres conditions pour d'autres colonnes si nécessaire
        return df

    def render_to_response(self, context, **response_kwargs):
        # Vérifier si la demande nécessite une réponse JSON
        if self.request.GET.get('format') == 'json':
            data = context.get('data_table', {})
            return JsonResponse(data)
        else:
            return super().render_to_response(context, **response_kwargs)