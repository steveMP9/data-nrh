from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
class FormulairePageView(TemplateView):
    template_name = 'formulaire/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formulaire"] = "active"
        return context