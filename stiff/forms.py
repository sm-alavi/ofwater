from django import forms
from .models import StiffTemplate, StiffTemplateLevel, StiffTemplateLevelIon
from analysis.models import Analysis, SamplePoint
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class StiffTemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        for k in self.fields:
            self.fields[k].widget.attrs['style'] = 'width:250px;'
            self.fields[k].widget.attrs['class'] = 'form-control'

    class Meta:
        model = StiffTemplate
        fields = ('name',)


class StiffTemplateLevelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        # self.fields['stiff_template'].disabled = True
        for k in self.fields:
            self.fields[k].widget.attrs['style'] = 'width:250px;'
            self.fields[k].widget.attrs['class'] = 'form-control'
        self.fields['stiff_template'].widget.attrs['readonly'] = True

    class Meta:
        model = StiffTemplateLevel
        fields = ('stiff_template', 'name',)


class StiffTemplateLevelIonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call to ModelForm constructor
        for k in self.fields:
            self.fields[k].widget.attrs['style'] = 'width:250px;'
            self.fields[k].widget.attrs['class'] = 'form-control'
        self.fields['stiff_template_level'].widget.attrs['readonly'] = True

    class Meta:
        model = StiffTemplateLevelIon
        fields = ('stiff_template_level', 'analysis',)


class StiffSettingsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ions = Analysis.objects.all()
        sp = SamplePoint.objects.all()
        stiff_template = StiffTemplate.objects.all()

        format = ['%Y-%m-%d']

        widget = forms.DateInput(
            format=format,
            attrs={'class': 'form-control form-control-sm',
                   'placeholder': 'Select a date',
                   'type': 'date'
                   })

        self.fields['dt_from'] = forms.DateField(label="From",
                                                 input_formats=format, widget=widget)
        self.fields['dt_to'] = forms.DateField(label="To",
                                               input_formats=format, widget=widget)
        self.fields['sp'] = forms.MultipleChoiceField(label="Sample Point", choices=((item.id, item.name) for item in sp),
                                                      widget=forms.SelectMultiple(attrs={
                                                          'class': 'form-control form-control-sm'})
                                                      )
        self.fields['stiff_template'] = forms.ChoiceField(label="Stiff Template", choices=((item.id, item.name) for item in stiff_template),
                                                          widget=forms.Select(attrs={
                                                              'class': 'form-control form-control-sm'}))
