from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from analysis.models import Analysis, TestAnalysis, Test, SamplePoint
from .models import StiffTemplate, StiffTemplateLevel, StiffTemplateLevelIon
from .forms import StiffTemplateForm, StiffTemplateLevelForm, StiffTemplateLevelIonForm, StiffSettingsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, TemplateView
from typing import Optional, Dict, Any, Type
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
# Create your views here.


@method_decorator(login_required, name="dispatch")
class StiffTemplateList(ListView):
    model = StiffTemplate
    context_object_name: Optional[str] = "data"
    template_name: str = "stiff/stifftemplate.html"


@method_decorator(login_required, name="dispatch")
class StiffTemplateCreate(CreateView):
    model = StiffTemplate
    context_object_name: Optional[str] = "form"
    form_class = StiffTemplateForm
    template_name: str = "form.html"
    success_url: Optional[str] = "/"

    def get_success_url(self) -> str:
        return redirect('stifftemplate').url


@method_decorator(login_required, name="dispatch")
class StiffTemplateUpdate(UpdateView):
    model = StiffTemplate
    context_object_name: Optional[str] = "form"
    form_class = StiffTemplateForm
    template_name: str = "form.html"
    success_url: Optional[str] = "/"

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs.get("pk"))

    def get_success_url(self) -> str:
        return redirect('stifftemplate').url


@method_decorator(login_required, name="dispatch")
class StiffTemplateDelete(DeleteView):
    model = StiffTemplate
    context_object_name: Optional[str] = "item"
    template_name: str = "delete.html"
    success_url: Optional[str] = "/"

    def get_success_url(self) -> str:
        return redirect('stifftemplate').url


@method_decorator(login_required, name="dispatch")
class StiffTemplateLevelList(ListView):
    model = StiffTemplateLevel
    template_name: str = "stiff/stifftemplatelevel.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        stifftemplate = StiffTemplate.objects.get(id=self.kwargs.get("pk"))
        stifftemplatelevel = StiffTemplateLevel.objects.filter(
            stiff_template=stifftemplate)
        context = {
            'data': stifftemplatelevel,
            'stifftemplate': stifftemplate
        }
        return context


@method_decorator(login_required, name="dispatch")
class StiffTemplateLevelCreate(CreateView):
    model = StiffTemplateLevel
    form_class = StiffTemplateLevelForm
    template_name: str = "form.html"
    context_object_name: Optional[str] = "form"
    success_url: Optional[str] = "/"

    def get_initial(self) -> Dict[str, Any]:
        initial = {'stiff_template': self.kwargs.get("pk")}
        return initial

    def get_success_url(self) -> str:
        return redirect('stifftemplatelevel', pk=self.kwargs.get("pk")).url


@method_decorator(login_required, name="dispatch")
class StiffTemplateLevelUpdate(UpdateView):
    model = StiffTemplateLevel
    template_name: str = "form.html"
    success_url: Optional[str] = "/"
    context_object_name: Optional[str] = "form"
    sifftemplatelevel: StiffTemplateLevel = None

    def get_success_url(self) -> str:
        idp = self.stifftemplatelevel.stiff_template_id
        return redirect('stifftemplatelevel', pk=str(idp))


@method_decorator(login_required, name="dispatch")
class StiffTemplateLevelDelete(DeleteView):
    model = StiffTemplateLevel
    template_name: str = "delete.html"
    context_object_name: Optional[str] = "item"
    success_url: Optional[str] = "/"


@method_decorator(login_required, name="dispatch")
class StiffTemplateLevelIonList(ListView):
    model = StiffTemplateLevelIon
    template_name: str = "stiff/stifftemplatelevelion.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        stifftemplatelevel = StiffTemplateLevel.objects.get(
            id=self.kwargs.get("pk"))
        stifftemplatelevelion = StiffTemplateLevelIon.objects.filter(
            stiff_template_level_id=stifftemplatelevel)
        context = {
            'data': stifftemplatelevelion,
            'stifftemplatelevel': stifftemplatelevel}
        return context


@method_decorator(login_required, name="dispatch")
class StiffTemplateLevelIonCreate(CreateView):
    model = StiffTemplateLevelIon
    form_class = StiffTemplateLevelIonForm
    context_object_name: Optional[str] = "form"
    template_name: str = "form.html"

    def get_initial(self) -> Dict[str, Any]:
        initial = {'stiff_template_level': self.kwargs.get("pk")}
        return initial

    def get_success_url(self) -> str:

        return redirect('stifftemplatelevelion', pk=self.kwargs.get("pk")).url


@method_decorator(login_required, name="dispatch")
class StiffTemplateLevelIonDelete(DeleteView):
    model = StiffTemplateLevelIon
    context_object_name: Optional[str] = "item"
    template_name: str = "delete.html"
    success_url: Optional[str] = "/"

    def get_success_url(self) -> str:
        id_ = self.get_object().stiff_template_level_id

        return redirect('stifftemplatelevel', pk=id_).url


@ login_required
def radarchartLoad(request, pk):
    testanalysis = TestAnalysis.objects.filter(test__well=int(pk))
    tests = Test.objects.filter(well=int(pk))
    analysis = Analysis.objects.all()
    samplepoints = SamplePoint.objects.all()
    context = {
        'testanalysis': testanalysis,
        'tests': tests,
        'analysis': analysis,
        'well_id': int(pk),
        'samplepoint': samplepoints,
    }
    return render(request, 'stiff/radarchart.html', context)


@ login_required
def radarchartFilter(request):
    if request.method == "POST":
        from_date = request.POST.get("from")
        to_date = request.POST.get("to")
        sp = request.POST.get("samplepoint")
        well_id = request.POST.get("well_id")

        tests = Test.objects.filter(
            Q(sampling_date__date__range=[from_date, to_date]),
            Q(samplepoint=sp),
            Q(well=int(well_id))
        )
        analysis = Analysis.objects.all()
        context = {
            'tests': [item.get_radar_chart_data() for item in tests],

            'analysis': list(analysis.values()),
        }

    return JsonResponse(context, safe=False)


@ login_required
def stiffcharttLoad(request, pk):

    if request.method == "POST":
        form = StiffSettingsForm(request.POST)
        if form.is_valid:
            dt_from = request.POST.get("dt_from")
            dt_to = request.POST.get("dt_to")
            samplepoint = request.POST.getlist("sp")
            well_id = int(pk)
            stifftemplate = request.POST.get("stiff_template")

            tests = Test.objects.filter(
                Q(sampling_date__date__range=[dt_from, dt_to]),
                Q(samplepoint__in=samplepoint),
                Q(well=int(well_id))
            )

            stifftemplatelevel = StiffTemplateLevel.objects.filter(
                stiff_template__id=stifftemplate).order_by('name')
            labels = []
            for item in stifftemplatelevel:

                label = {
                    'y': -int(item.name),
                    'label': '+'.join([ion.analysis.abbreviation for ion in item.stifftemplatelevelions.all() if ion.analysis.charge > 0]),
                    'alignment': 'near'
                }
                labels.append(label)

                label = {
                    'y': -int(item.name),
                    'label': '+'.join([ion.analysis.abbreviation for ion in item.stifftemplatelevelions.all() if ion.analysis.charge < 0]),
                    'alignment': 'far'
                }
                labels.append(label)

            analysis = Analysis.objects.all()
            context = {'form': form,
                       'tests': [item.get_stiff_chart_data(stifftemplate) for item in tests],
                       'analysis': list(analysis.values()),
                       'labels': labels
                       }
    else:
        form = StiffSettingsForm()
        context = {'form': form}

    return render(request, 'stiff/stiffchart.html', context)
