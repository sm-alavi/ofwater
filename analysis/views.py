from audioop import reverse
from importlib.metadata import metadata
from random import sample
from django.shortcuts import render, redirect
from . import models
from . import forms
from .models import Test, TestAnalysis, TestMetadata
from django.shortcuts import get_object_or_404
from django.db.models import Q, OuterRef
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from typing import Dict, Optional, Dict, Any
from django.urls import reverse
from django.db import transaction
# Create your views here.


@method_decorator(login_required, name="dispatch")
class AnalysisList(ListView):
    model = models.Analysis
    context_object_name: Optional[str] = "analysis"
    template_name: str = "analysis/analysis.html"


@method_decorator(login_required, name="dispatch")
class AnalysisCreate(CreateView):
    model = models.Analysis
    template_name: str = "form.html"
    form_class = forms.AnalysisForm
    success_url: Optional[str] = "/"


@method_decorator(login_required, name="dispatch")
class AnalysisUpdate(UpdateView):
    model = models.Analysis
    template_name: str = "form.html"
    form_class = forms.AnalysisForm
    success_url: Optional[str] = "/"

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs.get("id"))


@method_decorator(login_required, name="dispatch")
class AnalysisDelete(DeleteView):
    template_name: str = "delete.html"
    context_object_name: Optional[str] = "item"
    success_url: Optional[str] = "/"
    model = models.Analysis


@method_decorator(login_required, name="dispatch")
class SamplePointList(ListView):
    model = models.SamplePoint
    template_name: str = "analysis/samplepoint.html"
    context_object_name: Optional[str] = "samplepoint"


@method_decorator(login_required, name="dispatch")
class SamplePointCreate(CreateView):
    model = models.SamplePoint
    form_class = forms.SamplePointForm
    context_object_name: Optional[str] = "samplepoint"
    template_name: str = "form.html"
    success_url: Optional[str] = "/"


@method_decorator(login_required, name="dispatch")
class SamplePointUpdate(UpdateView):
    model = models.SamplePoint
    form_class = forms.SamplePointForm
    context_object_name: Optional[str] = "samplepoint"
    template_name: str = "form.html"
    success_url: Optional[str] = "/samplepoint"


@method_decorator(login_required, name="dispatch")
class SamplePointDelete(DeleteView):
    model = models.SamplePoint
    context_object_name: Optional[str] = "item"
    template_name: str = "delete.html"
    success_url: Optional[str] = "/samplepoint"


@method_decorator(login_required, name="dispatch")
class TestList(ListView):
    model = models.Test
    context_object_name: Optional[str] = "test"
    template_name: str = "analysis/test.html"


@method_decorator(login_required, name="dispatch")
class TestCreate(CreateView):
    model = models.Test
    form_class = forms.TestForm
    template_name: str = "form.html"
    success_url: Optional[str] = "/"


@method_decorator(login_required, name="dispatch")
class TestUpdate(UpdateView):
    template_name: str = "analysis/testupdate.html"
    form_class = forms.TestForm
    analysis_form_class = forms.TestAnalysis
    metadata_form_class = forms.TestMetadata
    success_url: Optional[str] = "/tests"
    model = Test

    def get_object(self):
        self.test = Test.objects.get(id=self.kwargs.get("pk"))
        self.testanalysis = TestAnalysis.objects.filter(
            test=self.kwargs.get("pk"))
        self.testmetadata = TestMetadata.objects.filter(
            test=self.kwargs.get("pk"))
        self.initials_analysis = {
            item.analysis.name: item.value for item in self.testanalysis}
        self.initials_metadata = {
            item.metadata.name: item.value for item in self.testmetadata}
        self.analysis = models.Analysis.objects.all()
        self.metadata = models.MetaData.objects.all()
        return super().get_object()

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*kwargs)

        if 'form' not in context:
            context['form'] = self.test_form_class(instance=self.test)
        if 'form_analysis' not in context:
            context['form_analysis'] = self.analysis_form_class(
                initial=self.initials_analysis)
        if 'form_meta' not in context:
            context['form_meta'] = self.metadata_form_class(
                initial=self.initials_metadata)

        return context

    def post(self, request, *args: Any, **kwargs: Any):
        self.object = self.get_object()
        form_test = self.form_class(request.POST, instance=self.test)
        form_analysis = self.analysis_form_class(request.POST)
        form_metadata = self.metadata_form_class(request.POST)

        if form_test.is_valid() and form_analysis.is_valid() and form_metadata.is_valid():
            # Save main form of data incluidng tests general data
            form_test.save()
            # Save test areverse + djangod for item in self.testanalysis]
            data = form_analysis.cleaned_data
            ids = [item.analysis_id for item in self.testanalysis]
            created = []
            update_dic = {}
            for item in self.analysis:
                val = data[item.name]
                if val == '':
                    val = None
                if item.id in ids:
                    update_dic[item.id] = val

                else:
                    created.append(models.TestAnalysis(test_id=self.kwargs.get('pk'), analysis_id=int(
                        item.id), value=val))

            with transaction.atomic():
                for k, v in update_dic.items():
                    TestAnalysis.objects.filter(
                        test=self.kwargs.get("pk"), analysis=k).update(value=v)

            models.TestAnalysis.objects.bulk_create(created)

            # save test metadata
            data = form_metadata.cleaned_data
            update_dic = {}
            for item in self.metadata:
                val = data[item.name]
                if val == '':
                    val = None
                update_dic[item.id] = val

                # obj, created = models.TestMetadata.objects.update_or_create(
                # test_id=self.kwargs.get('pk'), metadata_id=int(item.id), defaults={'value': val})
            with transaction.atomic():
                for k, v in update_dic.items():
                    TestMetadata.objects.filter(
                        test=self.kwargs.get("pk"), metadata=k).update(value=v)
        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('test')


@login_required
def testUpdate(request, pk):
    test = Test.objects.get(id=int(pk))
    testanalysis = TestAnalysis.objects.filter(test=int(pk))
    initials_analysis = {
        item.analysis.name: item.value for item in testanalysis}

    testmetadata = TestMetadata.objects.filter(test=int(pk))
    initials_metadata = {
        item.metadata.name: item.value for item in testmetadata}

    # Create form instances
    form = forms.TestForm(request.POST or None, instance=test)
    form_analysis = forms.TestAnalysis(
        request.POST or None, initial=initials_analysis)
    form_meta = forms.TestMetadata(
        request.POST or None, initial=initials_metadata)

    # Load all analysis & metadata
    analysis = models.Analysis.objects.all()
    metadata = models.MetaData.objects.all()

    if request.method == 'POST':
        if form.is_valid() and form_analysis.is_valid() and form_meta.is_valid():
            # Save main form of data incluidng tests general data
            form.save()
            # Save test analysis data
            data = form_analysis.cleaned_data

            ids = [item.id for item in testanalysis]
            created = []
            for item in analysis:
                val = data[item.name]
                if val == '':
                    val = None
                if item.id in ids:
                    testanalysis[ids.index(item.id)]['value'] = val
                else:
                    created.append(models.TestAnalysis(test_id=int(pk), analysis_id=int(
                        item.id), value=val))

            models.TestAnalysis.objects.bulk_update(testanalysis, ['value'])
            models.TestAnalysis.objects.bulk_create(created)

            # save test metadata
            data = form_meta.cleaned_data
            for item in metadata:
                val = data[item.name]
                if val == '':
                    val = None

                obj, created = models.TestMetadata.objects.update_or_create(
                    test_id=int(pk), metadata_id=int(item.id), defaults={'value': val})

            return redirect('test')

    else:

        context = {
            'form': form,
            'form_analysis': form_analysis,
            'form_meta': form_meta
        }

    return render(request, 'analysis/testupdate.html', context)


@method_decorator(login_required, name="dispatch")
class TestDelete(DeleteView):
    model = Test
    template_name: str = "delete.html"
    context_object_name: Optional[str] = "item"
    success_url: Optional[str] = "/test"


@method_decorator(login_required, name="dispatch")
class TestView(TemplateView):
    template_name: str = "analysis/testview.html"
    model = Test

    def get_context_data(self, **kwargs):
        # test = get_object_or_404(self.model, id=self.kwargs.get("pk"))
        test = Test.objects.get(id=self.kwargs.get("pk"))
        testanalysis = TestAnalysis.objects.filter(test=test)
        testmetadata = TestMetadata.objects.filter(test=test)

        context = {
            'test': test,
            'testanalysis': testanalysis,
            'testmetadata': testmetadata
        }

        return context


@ login_required
def testanalysisModify(request, pk):
    testanalysis = models.TestAnalysis.objects.filter(test=int(pk))
    initials = {item.analysis.name: item.value for item in testanalysis}
    form = forms.TestAnalysis(initial=initials)
    analysis = models.Analysis.objects.all()
    if request.method == "POST":
        form = forms.TestAnalysis(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            for item in analysis:
                val = data[item.name]
                if val == '':
                    val = None
                try:
                    testanalysis = models.TestAnalysis.objects.get(
                        Q(test=int(pk)) & Q(analysis=int(item.id)))
                    testanalysis.value = val
                    testanalysis.save()
                except ObjectDoesNotExist:
                    p = models.TestAnalysis(test=models.Test.objects.get(
                        id=int(pk)), analysis=models.Analysis.objects.get(id=int(item.id)), value=val)
                    p.save(force_insert=True)
            return redirect('test')

    context = {'form': form}
    return render(request, 'form.html', context)


@method_decorator(login_required, name="dispatch")
class MetaDataList(ListView):
    model = models.MetaData
    template_name: str = "analysis/metadata.html"
    context_object_name: Optional[str] = "metadata"


@method_decorator(login_required, name="dispatch")
class MetaDataCreate(CreateView):
    model = models.MetaData
    template_name: str = "form.html"
    context_object_name: Optional[str] = "form"
    form_class = forms.MetadataForm


@method_decorator(login_required, name="dispatch")
class MetaDataUpdate(UpdateView):
    model = models.MetaData
    template_name: str = "form.html"
    context_object_name: Optional[str] = "form"
    form_class = forms.MetadataForm

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs.get("pk"))


@method_decorator(login_required, name="dispatch")
class MetaDataDelete(DeleteView):
    model = models.MetaData
    context_object_name: Optional[str] = "item"
    template_name: str = "delete.html"
    success_url: Optional[str] = "/"


@ login_required
def testmetadataModify(request, pk):
    testmetadata = models.TestMetadata.objects.filter(test=int(pk))
    initials = {item.metadata.name: item.value for item in testmetadata}
    form = forms.TestMetadata(initial=initials)
    metadata = models.MetaData.objects.all()
    if request.method == "POST":
        form = forms.TestMetadata(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            for item in metadata:
                val = data[item.name]
                try:
                    testmetadata = models.TestMetadata.objects.get(
                        Q(test=int(pk)) & Q(metadata=int(item.id)))
                    testmetadata.value = val
                    testmetadata.save()
                except ObjectDoesNotExist:
                    p = models.TestMetadata(test=models.Test.objects.get(
                        id=int(pk)), metadata=models.MetaData.objects.get(id=int(item.id)), value=val)
                    p.save(force_insert=True)
            return redirect('test')

    context = {'form': form}
    return render(request, 'form.html', context)
