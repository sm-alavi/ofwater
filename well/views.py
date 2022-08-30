from audioop import reverse
from http.client import HTTPResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from . import models
from .models import Field, Well
from . import forms
from django.contrib import messages
from analysis.models import Test, SamplePoint
from dataclasses import dataclass
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from typing import Optional, Any, Dict
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.db.models import Transform
from django.db.models import FloatField


class AbsoluteValue(Transform):
    lookup_name = "abs"
    function = "ABS"


FloatField.register_lookup(AbsoluteValue)

# Create your views here.


@dataclass
class ModelItemsCount:
    title: str
    count: int
    url: str


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name: str = "well/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        field_test = Test.objects.values(
            'well__field__name').annotate(total=Count('id'))
        samplepoint_test = Test.objects.values(
            'samplepoint__name').annotate(total=Count('id'))
        wells = models.Well.objects.all()
        summary = [
            ModelItemsCount('Tests', Test.objects.count(), 'test'),
            ModelItemsCount('Wells', models.Well.objects.count(), 'well'),
            ModelItemsCount('Fields', models.Field.objects.count(), 'field'),
            ModelItemsCount('Sample Points',
                            SamplePoint.objects.count(), 'samplepoint'),
        ]

        cbe_green = Test.objects.filter(
            charge_balance_error__abs__range=[0, 5]).count()
        cbe_yellow = Test.objects.filter(
            charge_balance_error__abs__range=[5, 10]).count()
        cbe_red = Test.objects.filter(
            charge_balance_error__abs__gt=10).count()
        print(cbe_yellow)
        context = {
            'summary': summary,
            'wells_count': wells.count(),
            'field_test': field_test,
            'samplepoint_test': samplepoint_test,
            'wells': [item.get_json() for item in wells],
            'cbe_green': cbe_green,
            'cbe_yellow': cbe_yellow,
            'cbe_red': cbe_red
        }
        return context


@method_decorator(login_required, name="dispatch")
class WellList(ListView):
    template_name = "well/well.html"
    model = models.Well
    context_object_name: Optional[str] = "wells"


@method_decorator(login_required, name="dispatch")
class WellCreate(CreateView):
    template_name: str = 'form.html'
    success_url: Optional[str] = '/'
    form_class: forms.WellForm = forms.WellForm
    context_object_name: Optional[str] = 'form'

    def get_initial(self) -> Dict[str, Any]:

        return {'field': self.kwargs.get('id')} if 'id' in self.kwargs else super().get_initial()


@method_decorator(login_required, name="dispatch")
class WellUpdate(UpdateView):
    template_name: str = 'form.html'
    success_url: Optional[str] = '/wells'
    form_class: forms.WellForm = forms.WellForm
    context_object_name: Optional[str] = 'form'
    model = Well

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(self.model, id=id_)


@method_decorator(login_required, name="dispatch")
class WellDelete(DeleteView):
    model = Well
    context_object_name: Optional[str] = "item"
    template_name: str = "delete.html"
    success_url: Optional[str] = "/wells"


@method_decorator(login_required, name="dispatch")
class FieldList(ListView):
    model = Field
    context_object_name: Optional[str] = "fields"
    template_name: str = "well/field.html"

    def get_queryset(self):
        fields = models.Field.objects.all().annotate(c_count=Count('well'))
        return fields


@method_decorator(login_required, name="dispatch")
class FieldCreate(CreateView):
    template_name: str = 'form.html'
    success_url: Optional[str] = '/'
    form_class: forms.FieldForm = forms.FieldForm
    context_object_name: Optional[str] = 'form'
    model = Field


@method_decorator(login_required, name="dispatch")
class FieldUpdate(UpdateView):
    template_name: str = 'form.html'
    success_url: Optional[str] = '/fields'
    form_class: forms.FieldForm = forms.FieldForm
    context_object_name: Optional[str] = 'form'
    model = Field


@method_decorator(login_required, name="dispatch")
class FieldDelete(DeleteView):
    model = models.Field
    context_object_name: Optional[str] = "item"
    template_name: str = "delete.html"
    success_url: Optional[str] = "/fields"
